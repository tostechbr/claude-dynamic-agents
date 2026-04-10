# Notes Backend API

A FastAPI-based REST API for managing notes with full CRUD operations.

## Features

- Create, read, update, and delete notes
- Tag support for organizing notes
- Filter notes by tag
- Automatic timestamps (created_at, updated_at)
- CORS enabled for frontend integration
- Async SQLAlchemy with SQLite database
- Comprehensive test coverage

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application and routes
│   ├── models.py         # SQLAlchemy database models
│   ├── schemas.py        # Pydantic request/response schemas
│   ├── crud.py           # Database operations
│   └── database.py       # Database configuration
├── tests/
│   ├── conftest.py       # Pytest fixtures
│   └── test_notes.py     # API endpoint tests
├── pyproject.toml        # Poetry configuration
├── requirements.txt      # Pip requirements
└── run.sh               # Startup script
```

## Installation

### Using pip

```bash
pip install -r requirements.txt
```

### Using Poetry

```bash
poetry install
```

## Running the Server

### Using the shell script

```bash
chmod +x run.sh
./run.sh
```

### Using uvicorn directly

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
- `GET /` - Check API status

### Notes CRUD
- `POST /api/notes` - Create a new note (201)
- `GET /api/notes` - List all notes
- `GET /api/notes?tag=mytag` - Filter notes by tag
- `GET /api/notes/{id}` - Get a single note
- `PUT /api/notes/{id}` - Update a note
- `DELETE /api/notes/{id}` - Delete a note (204)

## API Examples

### Create a Note

```bash
curl -X POST http://localhost:8000/api/notes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Note",
    "content": "This is the content of my note",
    "tags": ["important", "work"]
  }'
```

Response (201):
```json
{
  "id": 1,
  "title": "My First Note",
  "content": "This is the content of my note",
  "tags": ["important", "work"],
  "created_at": "2026-04-09T12:00:00",
  "updated_at": "2026-04-09T12:00:00"
}
```

### List All Notes

```bash
curl http://localhost:8000/api/notes
```

Response:
```json
{
  "notes": [
    {
      "id": 1,
      "title": "My First Note",
      "content": "This is the content of my note",
      "tags": ["important", "work"],
      "created_at": "2026-04-09T12:00:00",
      "updated_at": "2026-04-09T12:00:00"
    }
  ],
  "total": 1,
  "count": 1
}
```

### Filter Notes by Tag

```bash
curl http://localhost:8000/api/notes?tag=important
```

### Get a Single Note

```bash
curl http://localhost:8000/api/notes/1
```

### Update a Note

```bash
curl -X PUT http://localhost:8000/api/notes/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "tags": ["work", "urgent"]
  }'
```

### Delete a Note

```bash
curl -X DELETE http://localhost:8000/api/notes/1
```

## Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app tests/
```

Run specific test:

```bash
pytest tests/test_notes.py::test_create_note
```

## Database

The application uses SQLite with async support:
- Database file: `notes.db` (created in the backend directory on first run)
- Uses async SQLAlchemy for non-blocking database operations
- Tables are auto-created on startup

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK` - Successful GET, PUT
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Invalid input (e.g., empty title, no fields in update)
- `404 Not Found` - Note doesn't exist
- `422 Unprocessable Entity` - Validation error

## Dependencies

- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **sqlalchemy** - ORM
- **aiosqlite** - Async SQLite driver
- **pydantic** - Data validation
- **pytest** - Testing framework
- **pytest-asyncio** - Async test support
- **httpx** - Async HTTP client for testing

## Configuration

### CORS Settings

Currently allows all origins. For production, update in `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Database

To enable SQL logging, change in `app/database.py`:

```python
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Enable SQL logging
)
```

## Notes

- No authentication required (as specified)
- Tags are stored as comma-separated strings in the database
- Tags are returned as arrays in API responses
- Timestamps are automatically managed
- Notes are ordered by `created_at` (newest first) in list responses
