from dataclasses import asdict, dataclass

@dataclass(frozen=True, slots=True)
class CompetitionCatalogItem:
    id: int
    name: str
    country: str
    priority: int
    enabled_by_default: bool = True

COMPETITION_CATALOG = (
    CompetitionCatalogItem(39, "Premier League", "England", 1),
    CompetitionCatalogItem(140, "La Liga", "Spain", 2),
    CompetitionCatalogItem(135, "Serie A", "Italy", 3),
    CompetitionCatalogItem(78, "Bundesliga", "Germany", 4),
    CompetitionCatalogItem(61, "Ligue 1", "France", 5),
    CompetitionCatalogItem(2, "UEFA Champions League", "Europe", 6),
    CompetitionCatalogItem(3, "UEFA Europa League", "Europe", 7),
    CompetitionCatalogItem(94, "Primeira Liga", "Portugal", 8, False),
    CompetitionCatalogItem(88, "Eredivisie", "Netherlands", 9, False),
)

def catalog_as_dicts() -> list[dict]:
    return [asdict(item) for item in COMPETITION_CATALOG]

def resolve_competitions(requested_ids: list[int] | None) -> list[CompetitionCatalogItem]:
    if requested_ids:
        wanted = set(requested_ids)
        return sorted([x for x in COMPETITION_CATALOG if x.id in wanted], key=lambda x: x.priority)
    return sorted([x for x in COMPETITION_CATALOG if x.enabled_by_default], key=lambda x: x.priority)
