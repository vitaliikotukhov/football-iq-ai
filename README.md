# Football IQ AI — Project Athena

Football IQ AI is an explainable football intelligence platform.

Its core rule is simple:

> Every prediction must explain **why**.

## Genesis v0.1 — Pack 1

This foundation includes:

- FastAPI backend
- PostgreSQL
- Docker Compose
- Configuration from environment variables
- Structured application logging
- Database health check
- `/`, `/health`, and `/version` endpoints
- Automated tests

## First run

1. Copy `.env.example` to `.env`.
2. Open a terminal in the repository root.
3. Run:

```powershell
docker compose up --build
```

4. Open:

- API documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health
- Version: http://localhost:8000/version

## Stop the application

```powershell
docker compose down
```

To also delete the local PostgreSQL data volume:

```powershell
docker compose down -v
```

## Project status

Release: **Genesis v0.1 — Pack 1**
