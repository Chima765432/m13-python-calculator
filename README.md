# Secure User Model API

A FastAPI project data layer: a SQLAlchemy User model with bcrypt password
hashing, Pydantic schemas for validation, and tests that run against
PostgreSQL locally and in CI. There are no routes yet; this module is the
foundation the API gets built on.

## What is here

- app/models/user.py: the User model. Unique username and email, a
  password_hash column, and hash and verify functions using bcrypt. Plain
  passwords are never stored.
- app/schemas/user.py: UserCreate validates input (username length, real
  email, minimum password length). UserRead shapes output and has no password
  field, so a hash cannot leak into a response.
- app/database.py and app/config.py: SQLAlchemy engine and session setup,
  with the database URL read from an environment variable.

## Run the tests locally

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    docker compose up -d
    pytest

The compose file starts PostgreSQL on port 5432. Unit tests cover hashing and
schema validation; integration tests store and read users against the real
database and prove the uniqueness constraints reject duplicates.

## CI/CD

Every push runs the full suite in GitHub Actions against a PostgreSQL service
container. If tests pass on main, the image is built and pushed to Docker Hub:

https://hub.docker.com/r/chima765432/m11-python-calculator

Pull it with:

    docker pull chima765432/m11-python-calculator:latest
