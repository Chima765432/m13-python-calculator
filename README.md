# Calculations API

A FastAPI REST API for users and calculations, backed by PostgreSQL through
SQLAlchemy, with Pydantic validation on every request and response.

## Endpoints

    POST   /users/register     create a user, password stored as a bcrypt hash
    POST   /users/login        verify credentials, 401 on failure

    GET    /calculations       browse
    GET    /calculations/{id}  read
    POST   /calculations       add, result computed on creation
    PUT    /calculations/{id}  edit, result recomputed
    DELETE /calculations/{id}  delete

Responses are shaped by Pydantic schemas, so a password hash cannot appear in
any response. Invalid input is rejected with a 422 before a route body runs:
an unknown calculation type, a zero divisor, a malformed email.

## Run it locally

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    docker compose up -d
    uvicorn main:app --reload

Open http://127.0.0.1:8000/docs for the interactive OpenAPI page. Each
endpoint can be run there with Try it out, which is the quickest manual check
that registration, login, and the calculation routes behave as expected.

## Run the tests

    pytest

Unit tests cover hashing, both schema sets, and the operation factory.
Integration tests hit every route against PostgreSQL: registration and
duplicate rejection, login success and failure, and the full create, read,
update, delete cycle for calculations including 404 and 422 cases.

## CI/CD

Every push runs the suite in GitHub Actions against a PostgreSQL service
container. If tests pass on main, the image is built and pushed to Docker Hub:

https://hub.docker.com/r/chima765432/m12-python-calculator

    docker pull chima765432/m12-python-calculator:latest
