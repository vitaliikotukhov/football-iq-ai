import logging
from datetime import date
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.integrations.api_football.client import ApiFootballClient
from app.models import Competition, Country, Season, Stadium, Team
from app.schemas.sync import LeagueSyncReport, SyncReport

logger = logging.getLogger(__name__)


def _clean_code(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text[:10] or None


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _country_by_name(db: Session, name: str) -> Country | None:
    return db.scalar(select(Country).where(Country.name == name))


def _country_by_code(db: Session, code: str) -> Country | None:
    return db.scalar(select(Country).where(Country.code == code))


def _upsert_country(
    db: Session,
    *,
    name: str,
    code: str | None,
) -> tuple[Country, bool, bool]:
    country = _country_by_name(db, name)
    if country is None and code:
        country = _country_by_code(db, code)

    if country is None:
        country = Country(name=name, code=code)
        db.add(country)
        db.flush()
        return country, True, False

    changed = False
    if country.name != name:
        country.name = name
        changed = True
    if code and country.code != code:
        country.code = code
        changed = True

    return country, False, changed


async def sync_countries(db: Session) -> SyncReport:
    payload = await ApiFootballClient().get("countries")
    rows = payload.get("response", [])

    report = SyncReport(resource="countries", received=len(rows))

    for item in rows:
        name = str(item.get("name") or "").strip()
        if not name:
            report.skipped += 1
            continue

        code = _clean_code(item.get("code"))
        _, created, updated = _upsert_country(
            db,
            name=name,
            code=code,
        )
        report.created += int(created)
        report.updated += int(updated)

    db.commit()
    return report


async def sync_league(
    db: Session,
    *,
    league_id: int,
    season_year: int,
) -> LeagueSyncReport:
    client = ApiFootballClient()

    league_payload = await client.get(
        "leagues",
        params={"id": league_id, "season": season_year},
    )
    league_rows = league_payload.get("response", [])
    if not league_rows:
        raise ValueError(
            f"No league data returned for league_id={league_id}, season={season_year}."
        )

    league_row = league_rows[0]
    provider_league = league_row.get("league") or {}
    provider_country = league_row.get("country") or {}
    provider_seasons = league_row.get("seasons") or []

    country_name = str(provider_country.get("name") or "International")
    country_code = _clean_code(provider_country.get("code"))
    country, country_created, _ = _upsert_country(
        db,
        name=country_name,
        code=country_code,
    )

    competition = db.scalar(
        select(Competition).where(Competition.api_id == league_id)
    )
    competition_created = competition is None
    if competition is None:
        competition = Competition(
            api_id=league_id,
            name=str(provider_league.get("name") or f"League {league_id}"),
            competition_type=str(provider_league.get("type") or "League"),
            country_id=country.id,
        )
        db.add(competition)
        db.flush()
    else:
        competition.name = str(
            provider_league.get("name") or competition.name
        )
        competition.competition_type = str(
            provider_league.get("type") or competition.competition_type
        )
        competition.country_id = country.id

    provider_season = next(
        (
            item
            for item in provider_seasons
            if int(item.get("year", -1)) == season_year
        ),
        {},
    )

    season_name = str(season_year)
    season = db.scalar(
        select(Season).where(
            Season.competition_id == competition.id,
            Season.name == season_name,
        )
    )
    season_created = season is None
    if season is None:
        season = Season(
            competition_id=competition.id,
            name=season_name,
            start_date=_parse_date(provider_season.get("start")),
            end_date=_parse_date(provider_season.get("end")),
            is_current=bool(provider_season.get("current", False)),
        )
        db.add(season)
        db.flush()
    else:
        season.start_date = _parse_date(provider_season.get("start"))
        season.end_date = _parse_date(provider_season.get("end"))
        season.is_current = bool(provider_season.get("current", False))

    teams_payload = await client.get(
        "teams",
        params={"league": league_id, "season": season_year},
    )
    team_rows = teams_payload.get("response", [])

    teams_created = 0
    teams_updated = 0
    stadiums_created = 0
    stadiums_updated = 0

    for item in team_rows:
        provider_team = item.get("team") or {}
        provider_venue = item.get("venue") or {}

        team_api_id = provider_team.get("id")
        if team_api_id is None:
            continue

        stadium = None
        venue_api_id = provider_venue.get("id")
        venue_name = str(provider_venue.get("name") or "").strip()

        if venue_api_id is not None or venue_name:
            if venue_api_id is not None:
                stadium = db.scalar(
                    select(Stadium).where(
                        Stadium.api_id == int(venue_api_id)
                    )
                )
            else:
                stadium = db.scalar(
                    select(Stadium).where(
                        Stadium.name == venue_name,
                        Stadium.country_id == country.id,
                    )
                )

            if stadium is None:
                stadium = Stadium(
                    api_id=int(venue_api_id) if venue_api_id is not None else None,
                    name=venue_name or f"Venue {venue_api_id}",
                    city=provider_venue.get("city"),
                    capacity=provider_venue.get("capacity"),
                    country_id=country.id,
                )
                db.add(stadium)
                db.flush()
                stadiums_created += 1
            else:
                stadium.name = venue_name or stadium.name
                stadium.city = provider_venue.get("city")
                stadium.capacity = provider_venue.get("capacity")
                stadium.country_id = country.id
                stadiums_updated += 1

        team = db.scalar(
            select(Team).where(Team.api_id == int(team_api_id))
        )
        if team is None:
            team = Team(
                api_id=int(team_api_id),
                name=str(provider_team.get("name") or f"Team {team_api_id}"),
                short_name=provider_team.get("code"),
                founded_year=provider_team.get("founded"),
                country_id=country.id,
                stadium_id=stadium.id if stadium else None,
            )
            db.add(team)
            teams_created += 1
        else:
            team.name = str(provider_team.get("name") or team.name)
            team.short_name = provider_team.get("code")
            team.founded_year = provider_team.get("founded")
            team.country_id = country.id
            team.stadium_id = stadium.id if stadium else team.stadium_id
            teams_updated += 1

    db.commit()

    logger.info(
        "League synchronization completed league_id=%s season=%s teams=%s",
        league_id,
        season_year,
        len(team_rows),
    )

    return LeagueSyncReport(
        league_id=league_id,
        season=season_year,
        competition_created=competition_created,
        season_created=season_created,
        country_created=country_created,
        teams_received=len(team_rows),
        teams_created=teams_created,
        teams_updated=teams_updated,
        stadiums_created=stadiums_created,
        stadiums_updated=stadiums_updated,
    )
