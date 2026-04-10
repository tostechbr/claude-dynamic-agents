# Frontend Integration Guide

This guide helps the backend team understand the frontend's API contract and integration points.

## Quick Start for Testers

```bash
cd /Users/tiago.santos/Documents/GitHub/claude-dynamic-agents/projects/notes-app/frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`  
Backend should run at `http://localhost:8000/api`

## API Contract

### Notes Object Structure

```typescript
interface Note {
  id: string              // UUID or any unique string
  title: string          // Note title (required)
  content: string        // Note body (required)
  tags: string[]         // Array of tag strings (optional, can be empty)
  created_at: string     // ISO 8601 timestamp
  updated_at: string     // ISO 8601 timestamp
}
```

### Endpoints Required

#### 1. GET /api/notes
**Purpose:** Fetch all notes

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "note-uuid-1",
      "title": "Example Note",
      "content": "This is the note content...",
      "tags": ["work", "important"],
      "created_at": "2024-04-09T10:30:00Z",
      "updated_at": "2024-04-09T10:30:00Z"
    }
  ]
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Database connection failed"
}
```

#### 2. POST /api/notes
**Purpose:** Create a new note

**Request Body:**
```json
{
  "title": "My New Note",
  "content": "This is the content",
  "tags": ["tag1", "tag2"]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "note-uuid-new",
    "title": "My New Note",
    "content": "This is the content",
    "tags": ["tag1", "tag2"],
    "created_at": "2024-04-09T10:30:00Z",
    "updated_at": "2024-04-09T10:30:00Z"
  }
}
```

**Validation Requirements:**
- `title` must be non-empty string
- `content` must be non-empty string
- `tags` must be array (can be empty)
- Return 400 with descriptive error if validation fails

#### 3. PUT /api/notes/:id
**Purpose:** Update an existing note

**Request Body:**
```json
{
  "title": "Updated Title",
  "content": "Updated content",
  "tags": ["newtag1"]
}
```

**Response:** Same as POST (updated Note object)

**Error Cases:**
- 404 if note ID doesn't exist
- 400 if validation fails
- Include descriptive error message

#### 4. DELETE /api/notes/:id
**Purpose:** Delete a note

**Response:**
```json
{
  "success": true
}
```

**Error Cases:**
- 404 if note ID doesn't exist
- Include descriptive error message

## API Response Format Contract

Every endpoint must return:

```typescript
{
  "success": boolean,
  "data?: any,
  "error?: string
}
```

**Rules:**
- `success: true` when operation succeeds
- Include `data` field with result on success
- `error` field only present on failure (string, not object)
- HTTP status codes should reflect success/failure:
  - 200/201 for success
  - 400 for validation errors
  - 404 for not found
  - 500 for server errors

## Frontend Error Handling

Frontend catches and handles these scenarios:

1. **Network errors**: Shows "Error loading notes" with retry button
2. **Validation errors**: Shows form validation messages
3. **API errors**: Displays error message to user
4. **Unexpected errors**: Generic "Failed to [action]" message

## Testing the Integration

### Create a Note
```bash
curl -X POST http://localhost:8000/api/notes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Note",
    "content": "Test content",
    "tags": ["test", "demo"]
  }'
```

Expected response:
- HTTP 201 or 200
- JSON with `success: true` and note data

### Get All Notes
```bash
curl http://localhost:8000/api/notes
```

Expected response:
- HTTP 200
- JSON array of notes

### Update a Note
```bash
curl -X PUT http://localhost:8000/api/notes/note-id \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated",
    "content": "New content",
    "tags": []
  }'
```

### Delete a Note
```bash
curl -X DELETE http://localhost:8000/api/notes/note-id
```

Expected response:
- HTTP 200
- JSON with `success: true`

## Test Data

For manual testing, the frontend works with:

**Minimal note:**
```json
{
  "id": "1",
  "title": "Hello",
  "content": "World",
  "tags": [],
  "created_at": "2024-04-09T10:00:00Z",
  "updated_at": "2024-04-09T10:00:00Z"
}
```

**Note with tags:**
```json
{
  "id": "2",
  "title": "Work Meeting",
  "content": "Discuss Q2 goals and timeline",
  "tags": ["work", "meeting", "urgent"],
  "created_at": "2024-04-08T14:30:00Z",
  "updated_at": "2024-04-09T10:00:00Z"
}
```

## Frontend Features Using Each Endpoint

| Feature | Endpoints Used | Expected Behavior |
|---------|---|---|
| Load notes on startup | GET | Displays all notes or empty state |
| Create note | POST | Form closes, note appears in list |
| Edit note | PUT | Note updates, list refreshes |
| Delete note | DELETE | Note disappears from list |
| Filter by tag | GET (cached) | Shows only matching notes |
| Refresh notes | GET | Fetches latest from backend |

## CORS Requirements

Frontend runs on `http://localhost:5173`, backend on `http://localhost:8000`.

Backend must enable CORS for:
- Origin: `http://localhost:5173` (or `*` for development)
- Methods: GET, POST, PUT, DELETE
- Headers: Content-Type

Example (if using FastAPI):
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Common Integration Issues

### Issue: "Cannot POST /api/notes"
- **Cause:** Backend endpoint not implemented
- **Fix:** Ensure all 4 endpoints exist

### Issue: "CORS error"
- **Cause:** Backend doesn't allow frontend origin
- **Fix:** Add CORS middleware to backend

### Issue: "Failed to fetch notes"
- **Cause:** Wrong response format
- **Fix:** Ensure response has `success` and `data` fields

### Issue: "Notes don't update after save"
- **Cause:** Response doesn't match expected Note structure
- **Fix:** Verify all Note fields present (id, title, content, tags, created_at, updated_at)

### Issue: "Tags don't filter"
- **Cause:** Notes have tags but filter shows nothing
- **Fix:** Ensure backend returns `tags` as array

## Performance Expectations

- GET /api/notes should return < 500ms for 50+ notes
- POST /api/notes should return < 200ms
- PUT/DELETE should return < 100ms
- No pagination implemented (MVP assumption: < 100 notes)

## Future Enhancements

Frontend is ready for:
- Search functionality (needs backend query param support)
- Sorting (needs backend sort options)
- Pagination (needs backend offset/limit)
- Categories/folders (needs new endpoint structure)
- Real-time updates (needs WebSocket support)
- Authentication (needs auth headers)

## Frontend Deployment

For production deployment:

1. **Build:** `npm run build` creates `dist/` folder
2. **Serve:** Deploy `dist/` contents as static files
3. **API:** Configure `VITE_API_BASE` environment variable or update vite.config.ts
4. **Backend:** Ensure CORS allows production domain

Example for production:
```typescript
// vite.config.ts
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: process.env.VITE_API_BASE || 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

## Questions or Issues?

Refer to:
- `README.md` - Project overview
- `DEVELOPMENT.md` - Development workflow
- `TESTING_CHECKLIST.md` - Test scenarios
- `src/api/notesApi.ts` - API client implementation
