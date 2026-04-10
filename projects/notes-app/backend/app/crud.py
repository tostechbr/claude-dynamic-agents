from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.models import Note
from app.schemas import NoteCreate, NoteUpdate


async def create_note(db: AsyncSession, note: NoteCreate) -> Note:
    """Create a new note in the database."""
    # Convert tags list to comma-separated string
    tags_str = ",".join(note.tags) if note.tags else ""

    db_note = Note(
        title=note.title,
        content=note.content,
        tags=tags_str,
    )
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    return db_note


async def get_note(db: AsyncSession, note_id: int) -> Optional[Note]:
    """Get a single note by ID."""
    result = await db.execute(select(Note).where(Note.id == note_id))
    return result.scalar_one_or_none()


async def get_all_notes(db: AsyncSession, tag: Optional[str] = None) -> List[Note]:
    """Get all notes, optionally filtered by tag."""
    query = select(Note)

    if tag:
        # Filter notes that contain the tag (case-insensitive)
        query = query.where(Note.tags.ilike(f"%{tag}%"))

    # Order by created_at descending (newest first)
    query = query.order_by(Note.created_at.desc())

    result = await db.execute(query)
    return result.scalars().all()


async def update_note(db: AsyncSession, note_id: int, note_update: NoteUpdate) -> Optional[Note]:
    """Update an existing note."""
    db_note = await get_note(db, note_id)

    if not db_note:
        return None

    # Only update fields that are provided (not None)
    if note_update.title is not None:
        db_note.title = note_update.title

    if note_update.content is not None:
        db_note.content = note_update.content

    if note_update.tags is not None:
        db_note.tags = ",".join(note_update.tags)

    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    return db_note


async def delete_note(db: AsyncSession, note_id: int) -> bool:
    """Delete a note by ID."""
    db_note = await get_note(db, note_id)

    if not db_note:
        return False

    await db.delete(db_note)
    await db.commit()
    return True
