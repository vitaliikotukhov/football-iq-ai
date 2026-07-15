# Genesis v0.1 — Pack 1

## Definition of done

- Docker Compose starts PostgreSQL and FastAPI.
- FastAPI waits for PostgreSQL to become healthy.
- `/health` reports the database connection.
- `/version` reports application version `0.1.0`.
- Swagger documentation is available at `/docs`.
- Root and version tests pass.

## Commit message

```text
feat(genesis): add Pack 1 application foundation
```
