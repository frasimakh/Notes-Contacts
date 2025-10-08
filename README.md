# Notes & Contacts Sample Project

This repository contains a small FastAPI project that mixes a few good
practices with intentional pitfalls to resemble a production-like code base for
analysis and discussion.

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

The application expects a PostgreSQL database. Default configuration values are
set in `app/core/config.py`. You can override them with environment variables.

## Project overview

* **Tech stack:** FastAPI, SQLAlchemy (sync), PostgreSQL, Alembic migrations,
  Pydantic schemas.
* **Domain:** Contacts have many notes. Endpoints cover CRUD operations,
  filtering, and simple search.
* **Intentional gaps:** Unbounded pagination, missing unique constraints,
  JSONB fields without indexes, naive datetime handling, inconsistent status
  codes, and potential N+1 issues when including notes.

These traits are left as-is to encourage code reading, architecture review, and
discussion about improvements.

## Running tests

```bash
pytest -q
```

Tests are intentionally incomplete and a bit brittle. They should spark
conversations about what else needs coverage.
