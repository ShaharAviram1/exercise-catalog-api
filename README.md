# Workout Exercise Catalog API

This project is a small FastAPI backend for Exercise 1 in the Advanced Programming Solutions course. It provides CRUD operations for a workout exercise catalog and keeps all data in memory.

## Project Structure

- `app/main.py` - FastAPI application entry point
- `app/models.py` - Pydantic models and enums
- `app/repository.py` - in-memory repository for exercises
- `app/routes.py` - API routes for CRUD operations
- `tests/test_exercises.py` - pytest test suite
- `pyproject.toml` - project configuration and dependencies

## Create and Activate a Virtual Environment with uv

```bash
uv venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
uv venv
.venv\Scripts\Activate.ps1
```

## Install Dependencies

```bash
uv sync --dev
```

## Run the API Locally

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

Interactive docs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Run the Tests

```bash
uv run pytest
```

## Available Endpoints

- `POST /exercises` - create an exercise
- `GET /exercises` - list all exercises
- `GET /exercises/{id}` - get one exercise by ID
- `PUT /exercises/{id}` - replace an existing exercise
- `DELETE /exercises/{id}` - delete an exercise

## Notes

- IDs are generated automatically starting from `1`.
- Data is stored only in memory, so restarting the server resets the catalog.
- Validation is handled with FastAPI and Pydantic, including enum checks, blank-name rejection, and muscle overlap rules.
