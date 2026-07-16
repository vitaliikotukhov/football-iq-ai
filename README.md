# Football IQ AI — Project Athena

Football IQ AI is an explainable football intelligence platform.

> Every prediction must explain why.

## Genesis v0.1 — Pack 4

Pack 4 adds the **Football Knowledge Builder**: a controlled, auditable workflow that turns the individual API-Football sync endpoints from Pack 3 into repeatable knowledge-building runs.

It includes:

- curated competition catalog;
- build plans before quota is consumed;
- dry-run mode that makes no provider requests;
- persistent run history;
- per-competition success and failure tracking;
- safe reruns and duplicate-resistant imports;
- request pacing between competitions;
- optional stop-on-error behavior;
- detailed run inspection endpoints.

Pack 4 can be installed before obtaining an API key. Without a key, use the catalog, plan, and dry-run endpoints.

## Run

```powershell
docker compose down
docker compose up --build
```

Open:

- Swagger: http://localhost:8000/docs
- Catalog: http://localhost:8000/builder/catalog
- Run history: http://localhost:8000/builder/runs

## Safe test without an API key

Use `POST /builder/build?dry_run=true` with:

```json
{
  "season": 2025,
  "competition_ids": [39],
  "include_countries": true,
  "stop_on_error": false
}
```
