# Calculation and User Model API

A FastAPI project data layer. Module 10 added a SQLAlchemy User model with
bcrypt password hashing and Pydantic validation. Module 11 adds a Calculation
model with a factory for the operation logic and schemas that validate input
before it reaches the database. There are no routes yet; endpoints arrive in
the next module.

## What is here

- app/models/user.py: User model. Unique username and email, bcrypt hash and
  verify functions. Plain passwords are never stored.
- app/models/calculation.py: Calculation model with fields a, b, type, result,
  and a user_id foreign key with delete cascade. compute() fills result using
  the factory.
- app/operations: the factory. A dictionary maps each type name (Add, Sub,
  Multiply, Divide) to its function; unknown types and division by zero raise
  ValueError.
- app/schemas: UserCreate and UserRead; CalculationCreate validates the type
  against an enum and rejects a zero divisor, CalculationRead serializes rows
  including result and user_id.

## Run the tests locally

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    docker compose up -d
    pytest

The compose file starts PostgreSQL on port 5432. Unit tests cover hashing,
both schema sets, and the factory. Integration tests store users and
calculations in the real database, verify computed results, the foreign key
link, and that deleting a user cascades to their calculations.

## CI/CD

Every push runs the suite in GitHub Actions against a PostgreSQL service
container. If tests pass on main, the image is built and pushed to Docker Hub:

https://hub.docker.com/r/chima765432/m11-python-calculator

Pull it with:

    docker pull chima765432/m11-python-calculator:latest
