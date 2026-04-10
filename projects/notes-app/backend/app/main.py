from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db, init_db
from app.schemas import NoteCreate, NoteUpdate, NoteResponse, NoteListResponse
from app import crud

app = FastAPI(
    title="Notes API",
    description="A simple CRUD API for notes",
    version="0.1.0",
)

# Enable CORS for all origins (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    await init_db()


@app.get("/", tags=["health"])
async def root():
    """Health check endpoint."""
    return {"message": "Notes API is running", "version": "0.1.0"}


@app.post("/api/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED, tags=["notes"])
async def create_note(note: NoteCreate, db: AsyncSession = Depends(get_db)):
    """Create a new note."""
    db_note = await crud.create_note(db, note)
    return db_note.to_dict()


@app.get("/api/notes", response_model=NoteListResponse, tags=["notes"])
async def list_notes(tag: Optional[str] = Query(None, description="Filter by tag"), db: AsyncSession = Depends(get_db)):
    """
    List all notes.

    - **tag** (optional): Filter notes by tag
    """
    notes = await crud.get_all_notes(db, tag=tag)
    return NoteListResponse(
        notes=[note.to_dict() for note in notes],
        total=len(notes),
        count=len(notes),
    )


@app.get("/api/notes/{note_id}", response_model=NoteResponse, tags=["notes"])
async def get_note(note_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single note by ID."""
    db_note = await crud.get_note(db, note_id)

    if not db_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found",
        )

    return db_note.to_dict()


@app.put("/api/notes/{note_id}", response_model=NoteResponse, tags=["notes"])
async def update_note(note_id: int, note_update: NoteUpdate, db: AsyncSession = Depends(get_db)):
    """Update a note by ID."""
    # Validate that at least one field is provided
    if not any([note_update.title, note_update.content, note_update.tags is not None]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field (title, content, or tags) must be provided for update",
        )

    db_note = await crud.update_note(db, note_id, note_update)

    if not db_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found",
        )

    return db_note.to_dict()


@app.delete("/api/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["notes"])
async def delete_note(note_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a note by ID."""
    deleted = await crud.delete_note(db, note_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found",
        )

    return None
