# Job Tracker API

REST API for tracking job applications (company, role, status, date, link, notes), built to practice a typical backend setup: FastAPI, SQLAlchemy, PostgreSQL, automated tests and Docker.

Requires Docker Desktop.

```powershell
docker compose up --build
```

Open http://localhost:8000/docs for the interactive API documentation. Data is stored in PostgreSQL in a named Docker volume, so it survives restarts. `docker compose down -v` deletes it.

The database credentials in `docker-compose.yml` are for local development only.

# Endpoints

| Method | Path | Description |
| POST | `/applications` | Create an application |
| GET | `/applications` | List applications, optionally filtered with `?status=applied` |
| GET | `/applications/{id}` | Get one application |
| PATCH | `/applications/{id}` | Update only the fields you send |
| DELETE | `/applications/{id}` | Delete an application |

Status values: `saved`, `applied`, `interview`, `offer`, `rejected`.

# Tests

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m pytest -q
```

Tests run against an in-memory SQLite database, so no Docker is needed. They cover creating, reading, filtering, partial updates, deleting, and validation (invalid statuses and `null` in required fields return 422).

## Design notes

- Pydantic schemas validate input. Separate create, update and output models keep partial updates safe.
- `PATCH` applies only fields the client sent. Sending `null` for a required field is rejected with a 422 instead of failing in the database.
- The database URL comes from the `DATABASE_URL` environment variable and defaults to local SQLite for development.

## Not done yet

Authentication, database migrations (tables are created at startup), and a CI pipeline.