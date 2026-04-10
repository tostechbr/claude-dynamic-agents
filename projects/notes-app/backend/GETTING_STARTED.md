# Getting Started with Notes API Backend

## Quick Start (5 minutes)

### 1. Install Dependencies

Using pip:
```bash
pip install -r requirements.txt
```

Using poetry:
```bash
poetry install
```

### 2. Start the Server

Option A - Using the run script:
```bash
chmod +x run.sh
./run.sh
```

Option B - Using uvicorn directly:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Option C - Using make:
```bash
make dev
```

Option D - Using Docker:
```bash
docker-compose up
```

### 3. Verify It's Working

Open your browser and go to:
```
http://localhost:8000
```

You should see:
```json
{
  "message": "Notes API is running",
  "version": "0.1.0"
}
```

## API Documentation

Once the server is running, visit:
```
http://localhost:8000/docs
```

This opens the interactive Swagger UI where you can:
- See all endpoints
- Read parameter descriptions
- Try endpoints with the UI
- View request/response schemas

Alternative (ReDoc):
```
http://localhost:8000/redoc
```

## Creating Your First Note

```bash
curl -X POST http://localhost:8000/api/notes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Note",
    "content": "Hello, Notes API!",
    "tags": ["hello", "first"]
  }'
```

Response (201 Created):
```json
{
  "id": 1,
  "title": "My First Note",
  "content": "Hello, Notes API!",
  "tags": ["hello", "first"],
  "created_at": "2026-04-09T14:30:00",
  "updated_at": "2026-04-09T14:30:00"
}
```

## Running Tests

### Run all tests:
```bash
pytest -v
```

### Run with coverage report:
```bash
pytest --cov=app --cov-report=html
```

### Run specific test:
```bash
pytest tests/test_notes.py::test_create_note -v
```

### Run using make:
```bash
make test
make test-cov
```

## Project Structure

```
backend/
├── app/                    # Main application
│   ├── main.py            # FastAPI app and routes
│   ├── models.py          # Database models
│   ├── schemas.py         # Pydantic schemas
│   ├── crud.py            # Database operations
│   └── database.py        # DB configuration
├── tests/                 # Test suite
│   ├── conftest.py        # Test setup
│   └── test_notes.py      # API tests
├── Makefile               # Common commands
├── README.md              # Full documentation
├── GETTING_STARTED.md     # This file
├── IMPLEMENTATION_SUMMARY.md # Implementation details
├── Dockerfile             # Docker image
├── docker-compose.yml     # Docker compose config
├── pyproject.toml         # Poetry config
├── requirements.txt       # Pip requirements
└── run.sh                # Start script
```

## Common Commands

### Development
```bash
make dev              # Start dev server with auto-reload
make test             # Run tests
make test-cov         # Run tests with coverage
make lint             # Check Python syntax
make clean            # Clean __pycache__, .pytest_cache
```

### Database
```bash
# Database file is auto-created in backend/ directory as notes.db
# To reset database, simply delete notes.db and restart server
```

### Docker
```bash
# Build and run with Docker Compose
docker-compose up

# Build image manually
docker build -t notes-api .

# Run container
docker run -p 8000:8000 notes-api
```

## Directory Explanation

| File/Dir | Purpose |
|----------|---------|
| `app/main.py` | FastAPI application with all endpoints |
| `app/models.py` | SQLAlchemy database model for Note |
| `app/schemas.py` | Pydantic validation schemas |
| `app/crud.py` | Database operations (Create, Read, Update, Delete) |
| `app/database.py` | Async SQLAlchemy setup |
| `tests/` | Test suite with 15+ test cases |
| `pyproject.toml` | Poetry dependency management |
| `requirements.txt` | Pip dependency list |
| `Makefile` | Convenient command shortcuts |
| `README.md` | Comprehensive documentation |
| `Dockerfile` | Docker container configuration |
| `docker-compose.yml` | Multi-container setup |

## Environment Setup

### Python Version
Requires Python 3.9 or higher:
```bash
python3 --version
```

### Virtual Environment (Recommended)

#### Using venv:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Using poetry:
```bash
poetry install
poetry shell
```

## Troubleshooting

### Port Already in Use
If port 8000 is in use, specify a different port:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### Database Issues
To reset the database:
```bash
rm notes.db
# Restart the server, it will create a new database
```

### Import Errors
Make sure you're in the backend directory:
```bash
cd projects/notes-app/backend
```

### Test Failures
Install test dependencies:
```bash
pip install -r requirements.txt
```

## Next Steps

1. **Explore the API** - Go to http://localhost:8000/docs
2. **Create some notes** - Use the Swagger UI or curl
3. **Read the code** - Check `app/main.py` to see endpoint implementations
4. **Run the tests** - `pytest -v` to verify everything works
5. **Connect a frontend** - The API is ready to use!

## API Reference

### Create a Note
```
POST /api/notes
Content-Type: application/json

{
  "title": "string (required)",
  "content": "string (required)",
  "tags": ["optional", "tags"]
}

Returns: 201 Created with note data
```

### List All Notes
```
GET /api/notes
GET /api/notes?tag=mytag

Returns: 200 OK with array of notes
```

### Get Single Note
```
GET /api/notes/{id}

Returns: 200 OK or 404 Not Found
```

### Update Note
```
PUT /api/notes/{id}
Content-Type: application/json

{
  "title": "updated title",
  "content": "updated content",
  "tags": ["new", "tags"]
}

Returns: 200 OK or 404 Not Found
```

### Delete Note
```
DELETE /api/notes/{id}

Returns: 204 No Content or 404 Not Found
```

## Support

- Check README.md for detailed documentation
- Review test cases in tests/test_notes.py for examples
- See IMPLEMENTATION_SUMMARY.md for technical details

## Key Features

- FastAPI with async/await
- SQLAlchemy with async SQLite
- Pydantic validation
- CORS enabled
- Comprehensive error handling
- Tag filtering support
- Automatic timestamps
- Full test coverage
- Docker ready
