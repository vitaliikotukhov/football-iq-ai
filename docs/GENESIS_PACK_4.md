# Genesis v0.1 — Pack 4

## Goal

Turn individual provider synchronization calls into a controlled Football Knowledge Builder.

## Workflow

Catalog → Plan → Dry Run → Persistent Build Run → Countries → Competitions → Seasons → Teams → Stadiums → Results.

## New endpoints

- `GET /builder/catalog`
- `POST /builder/plan`
- `POST /builder/build`
- `GET /builder/runs`

## Request estimates

The current builder estimates one provider call for countries and two calls per competition (`leagues` and `teams`). API-Sports exposes account quota information through its status endpoint and returns rate-limit information with responses, so planning and pacing are treated as first-class operational concerns.

## Commit message

`feat(builder): add Genesis Pack 4 football knowledge builder`
