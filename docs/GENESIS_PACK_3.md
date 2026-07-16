# Genesis v0.1 — Pack 3

## Goal

Connect Project Athena to API-Football and safely import real football data.

## Provider

Base URL:

```text
https://v3.football.api-sports.io
```

Authentication header:

```text
x-apisports-key
```

The API key stays only in the local `.env` file and must never be committed.

## New endpoints

- `GET /sync/provider-status`
- `POST /sync/countries`
- `POST /sync/league/{league_id}?season=YYYY`

## League synchronization

A league synchronization imports or updates:

- country
- competition
- season
- teams
- stadiums

The operation is idempotent: running the same synchronization again updates
existing records instead of intentionally creating duplicates.

## Definition of done

- Provider status confirms a valid API key.
- Countries synchronize successfully.
- One selected league and season synchronize successfully.
- `/knowledge/summary` shows stored records.
- API key is absent from Git history and application responses.

## Commit message

```text
feat(sync): add Genesis Pack 3 API-Football acquisition engine
```
