from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    """Schema for creating a new note."""
    title: str = Field(..., min_length=1, max_length=255, description="Note title")
    content: str = Field(..., min_length=1, description="Note content")
    tags: Optional[List[str]] = Field(default=None, description="Optional list of tags")


class NoteUpdate(BaseModel):
    """Schema for updating an existing note."""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Note title")
    content: Optional[str] = Field(None, min_length=1, description="Note content")
    tags: Optional[List[str]] = Field(None, description="Optional list of tags")


class NoteResponse(BaseModel):
    """Schema for note response."""
    id: int
    title: str
    content: str
    tags: List[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class NoteListResponse(BaseModel):
    """Schema for listing notes."""
    notes: List[NoteResponse]
    total: int
    count: int
