import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test the health check endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Notes API is running"


@pytest.mark.asyncio
async def test_create_note(client: AsyncClient):
    """Test creating a new note."""
    note_data = {
        "title": "Test Note",
        "content": "This is a test note",
        "tags": ["test", "sample"],
    }
    response = await client.post("/api/notes", json=note_data)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "This is a test note"
    assert data["tags"] == ["test", "sample"]
    assert data["id"] is not None
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


@pytest.mark.asyncio
async def test_create_note_without_tags(client: AsyncClient):
    """Test creating a note without tags."""
    note_data = {
        "title": "Note Without Tags",
        "content": "Content without tags",
    }
    response = await client.post("/api/notes", json=note_data)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Note Without Tags"
    assert data["tags"] == []


@pytest.mark.asyncio
async def test_create_note_validation_error(client: AsyncClient):
    """Test creating a note with invalid data."""
    # Missing required fields
    response = await client.post("/api/notes", json={"title": ""})
    assert response.status_code == 422

    # Missing content
    response = await client.post("/api/notes", json={"title": "Test"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_note(client: AsyncClient):
    """Test retrieving a specific note."""
    # Create a note first
    note_data = {
        "title": "Get Note Test",
        "content": "Content for get test",
        "tags": ["gettest"],
    }
    create_response = await client.post("/api/notes", json=note_data)
    note_id = create_response.json()["id"]

    # Get the note
    response = await client.get(f"/api/notes/{note_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == note_id
    assert data["title"] == "Get Note Test"
    assert data["content"] == "Content for get test"
    assert data["tags"] == ["gettest"]


@pytest.mark.asyncio
async def test_get_note_not_found(client: AsyncClient):
    """Test retrieving a non-existent note."""
    response = await client.get("/api/notes/9999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_all_notes(client: AsyncClient):
    """Test listing all notes."""
    # Create multiple notes
    notes_data = [
        {
            "title": "Note 1",
            "content": "Content 1",
            "tags": ["tag1"],
        },
        {
            "title": "Note 2",
            "content": "Content 2",
            "tags": ["tag2"],
        },
        {
            "title": "Note 3",
            "content": "Content 3",
            "tags": ["tag1", "tag2"],
        },
    ]

    for note_data in notes_data:
        await client.post("/api/notes", json=note_data)

    # List all notes
    response = await client.get("/api/notes")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert data["count"] == 3
    assert len(data["notes"]) == 3


@pytest.mark.asyncio
async def test_list_notes_filter_by_tag(client: AsyncClient):
    """Test listing notes filtered by tag."""
    notes_data = [
        {
            "title": "Note with tag1",
            "content": "Content 1",
            "tags": ["tag1", "common"],
        },
        {
            "title": "Note with tag2",
            "content": "Content 2",
            "tags": ["tag2"],
        },
        {
            "title": "Another with tag1",
            "content": "Content 3",
            "tags": ["tag1"],
        },
    ]

    for note_data in notes_data:
        await client.post("/api/notes", json=note_data)

    # Filter by tag1
    response = await client.get("/api/notes?tag=tag1")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert all("tag1" in note["tags"] for note in data["notes"])


@pytest.mark.asyncio
async def test_update_note(client: AsyncClient):
    """Test updating a note."""
    # Create a note
    note_data = {
        "title": "Original Title",
        "content": "Original Content",
        "tags": ["original"],
    }
    create_response = await client.post("/api/notes", json=note_data)
    note_id = create_response.json()["id"]

    # Update the note
    update_data = {
        "title": "Updated Title",
        "content": "Updated Content",
        "tags": ["updated", "modified"],
    }
    response = await client.put(f"/api/notes/{note_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == note_id
    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated Content"
    assert data["tags"] == ["updated", "modified"]


@pytest.mark.asyncio
async def test_partial_update_note(client: AsyncClient):
    """Test partially updating a note."""
    # Create a note
    note_data = {
        "title": "Original Title",
        "content": "Original Content",
        "tags": ["original"],
    }
    create_response = await client.post("/api/notes", json=note_data)
    note_id = create_response.json()["id"]

    # Partially update (only title)
    update_data = {"title": "Updated Title"}
    response = await client.put(f"/api/notes/{note_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["content"] == "Original Content"  # Should remain unchanged
    assert data["tags"] == ["original"]  # Should remain unchanged


@pytest.mark.asyncio
async def test_update_note_not_found(client: AsyncClient):
    """Test updating a non-existent note."""
    update_data = {"title": "New Title"}
    response = await client.put("/api/notes/9999", json=update_data)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_note_no_fields(client: AsyncClient):
    """Test updating with no fields raises error."""
    # Create a note
    note_data = {
        "title": "Test",
        "content": "Content",
    }
    create_response = await client.post("/api/notes", json=note_data)
    note_id = create_response.json()["id"]

    # Try to update with empty data
    response = await client.put(f"/api/notes/{note_id}", json={})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_delete_note(client: AsyncClient):
    """Test deleting a note."""
    # Create a note
    note_data = {
        "title": "Note to Delete",
        "content": "This will be deleted",
    }
    create_response = await client.post("/api/notes", json=note_data)
    note_id = create_response.json()["id"]

    # Delete the note
    response = await client.delete(f"/api/notes/{note_id}")
    assert response.status_code == 204

    # Verify it's deleted
    response = await client.get(f"/api/notes/{note_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_note_not_found(client: AsyncClient):
    """Test deleting a non-existent note."""
    response = await client.delete("/api/notes/9999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_note_timestamps_ordering(client: AsyncClient):
    """Test that notes are ordered by created_at descending."""
    import asyncio

    notes_data = [
        {"title": "Note 1", "content": "Content 1"},
        {"title": "Note 2", "content": "Content 2"},
        {"title": "Note 3", "content": "Content 3"},
    ]

    # Create notes with small delays to ensure timestamp differences
    for note_data in notes_data:
        await client.post("/api/notes", json=note_data)
        await asyncio.sleep(0.01)

    # List notes
    response = await client.get("/api/notes")
    data = response.json()
    notes = data["notes"]

    # Verify ordering (most recent first)
    for i in range(len(notes) - 1):
        assert notes[i]["created_at"] >= notes[i + 1]["created_at"]
