# Exercise Service for a Workout Planning System

This project is a small FastAPI Exercise Service for Exercise 1 in the Advanced Programming Solutions course. It forms the foundation of a larger Workout Planning System by providing CRUD operations for an exercise catalog and keeping all data in memory.

## Design & Development Approach

This project was developed with a focus on clean system design, controlled scope, and iterative refinement.

The initial step was to define a simple but extensible domain. An Exercise resource was chosen as the core entity, representing the definition of a movement (e.g., Bench Press, Squat). This aligns well with the assignment requirement of building a single, well-defined resource while also serving as a strong foundation for future extensions such as workout planning and recommendation features.

### Modeling Decisions

Several design choices were made to ensure data consistency and clarity:

- **Enums over free text** were used for muscle groups, equipment, and difficulty to prevent invalid or inconsistent inputs.
- **Primary and secondary muscle groups** were modeled separately to reflect real-world exercise mechanics and allow more expressive queries in the future.
- **Validation rules** were added at both the field and model level, including:
  - rejecting empty or whitespace-only names
  - enforcing at least one primary muscle
  - preventing overlap between primary and secondary muscle groups
  - validating media URLs when provided

One example of iterative refinement was the muscle taxonomy: an initial generic `"legs"` category was replaced with more specific `"quadriceps"` and `"hamstrings"` values to avoid mixed granularity and improve consistency.

### Architecture

The project follows a simple separation of concerns:

- `models` define the data schema and validation rules
- `repository` handles storage and data access
- `routes` define the API layer and HTTP behavior

This structure keeps responsibilities clear and allows future changes (e.g., replacing in-memory storage with a database) without affecting the API layer.

### Development Workflow

Development was done iteratively, treating each change as a small, testable step. AI tools were used as a coding assistant to accelerate implementation, but all core decisions — including data modeling, validation rules, API design, and test coverage — were defined and reviewed manually.

Rather than generating the entire project in one step, the system was built and refined in stages:
- defining the data model and constraints
- implementing CRUD behavior
- adding validation and edge-case handling
- expanding test coverage
- refining naming and consistency

All generated code was reviewed and adjusted to ensure correctness, clarity, and alignment with the intended design.

### Future Direction

This service is designed as the foundation for a larger **Workout Planning System**. In future exercises, it can be extended with:
- a Workout service for composing exercise plans
- a user interface for browsing and managing exercises
- additional services such as recommendation or analytics

By keeping the current implementation focused and well-structured, it can be easily integrated into a broader multi-service architecture.

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

- `POST /exercises` - create an exercise, returns `201 Created`
- `GET /exercises` - list all exercises
- `GET /exercises/{id}` - get one exercise by ID, returns `404 Not Found` if the exercise does not exist
- `PUT /exercises/{id}` - fully replace an existing exercise, returns `404 Not Found` if the exercise does not exist. This endpoint performs a full replacement of the exercise object. All fields must be provided.
- `DELETE /exercises/{id}` - delete an exercise, returns `204 No Content`, or `404 Not Found` if the exercise does not exist

## Example Request Body

```json
{
  "name": "Squat",
  "primary_muscles": ["quadriceps"],
  "secondary_muscles": ["glutes", "hamstrings"],
  "equipment": "barbell",
  "difficulty": "beginner",
  "instructions": "Keep your chest up and drive through your feet.",
  "media_url": "https://example.com/squat"
}
```

## Notes

- IDs are generated automatically starting from `1`.
- Data is stored only in memory, so restarting the server resets the catalog.
- Validation is handled with FastAPI and Pydantic, including enum checks, blank-name rejection, and muscle overlap rules.

## Future Direction

- **EX1:** Exercise Service with validation, CRUD endpoints, tests, and in-memory storage.
- **EX2:** User interface for browsing existing exercises and adding new ones.
- **EX3:** Persistence layer for durable storage.
- **EX3:** Workout Service for composing exercise plans.
- **EX3:** Optional recommendation or assistant service.
