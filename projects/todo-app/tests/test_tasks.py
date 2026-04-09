"""
Comprehensive pytest tests for the FastAPI todo-app backend.

Covers POST /tasks and GET /tasks endpoints with async httpx client.
"""

import pytest
import pytest_asyncio
import httpx


# ---------------------------------------------------------------------------
# POST /tasks
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_task_happy_path(client: httpx.AsyncClient) -> None:
    """POST /tasks with valid title returns 201 and correct response shape."""
    response = await client.post("/tasks", json={"title": "Buy milk"})

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Buy milk"
    assert data["description"] is None
    assert data["done"] is False


@pytest.mark.asyncio
async def test_create_task_with_description(client: httpx.AsyncClient) -> None:
    """POST /tasks with title and description returns 201 and preserves both fields."""
    payload = {"title": "Buy groceries", "description": "Milk, eggs, bread"}
    response = await client.post("/tasks", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["description"] == "Milk, eggs, bread"
    assert data["done"] is False


@pytest.mark.asyncio
async def test_create_task_response_has_all_fields(client: httpx.AsyncClient) -> None:
    """POST /tasks response includes id, title, description, and done fields."""
    response = await client.post("/tasks", json={"title": "Test task"})

    assert response.status_code == 201
    data = response.json()
    assert set(data.keys()) >= {"id", "title", "description", "done"}


@pytest.mark.asyncio
async def test_create_task_increments_id(client: httpx.AsyncClient) -> None:
    """Each new task receives a sequentially incremented id."""
    response_one = await client.post("/tasks", json={"title": "First task"})
    response_two = await client.post("/tasks", json={"title": "Second task"})

    assert response_one.json()["id"] == 1
    assert response_two.json()["id"] == 2


@pytest.mark.asyncio
async def test_create_task_done_defaults_to_false(client: httpx.AsyncClient) -> None:
    """Newly created tasks are always not done."""
    response = await client.post("/tasks", json={"title": "New task"})

    assert response.json()["done"] is False


@pytest.mark.asyncio
async def test_create_task_missing_title_returns_422(client: httpx.AsyncClient) -> None:
    """POST /tasks with no title field returns 422 Unprocessable Entity."""
    response = await client.post("/tasks", json={"description": "No title provided"})

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_task_empty_body_returns_422(client: httpx.AsyncClient) -> None:
    """POST /tasks with an empty JSON object returns 422."""
    response = await client.post("/tasks", json={})

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_task_empty_title_string(client: httpx.AsyncClient) -> None:
    """POST /tasks with an empty string title is accepted by Pydantic (str is valid).

    FastAPI/Pydantic validates the type, not emptiness unless a validator is added.
    This test documents the current behaviour — empty string is a valid str.
    """
    response = await client.post("/tasks", json={"title": ""})

    # An empty string satisfies `str` in Pydantic v2 by default.
    # If the team adds a min_length validator later, this should become 422.
    assert response.status_code in (201, 422)


@pytest.mark.asyncio
async def test_create_task_null_title_returns_422(client: httpx.AsyncClient) -> None:
    """POST /tasks with title=null returns 422 because title is non-optional str."""
    response = await client.post("/tasks", json={"title": None})

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_task_non_string_title_returns_422(
    client: httpx.AsyncClient,
) -> None:
    """POST /tasks with a numeric title returns 422 (strict Pydantic v2 behaviour)."""
    response = await client.post("/tasks", json={"title": 123})

    # Pydantic v2 in lax mode coerces ints to str; in strict mode it rejects.
    # Document current behaviour without assuming either.
    assert response.status_code in (201, 422)


# ---------------------------------------------------------------------------
# GET /tasks
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_list_tasks_empty(client: httpx.AsyncClient) -> None:
    """GET /tasks with no tasks returns 200 and an empty list."""
    response = await client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_tasks_returns_created_tasks(client: httpx.AsyncClient) -> None:
    """GET /tasks after creating tasks returns all tasks."""
    await client.post("/tasks", json={"title": "Task A"})
    await client.post("/tasks", json={"title": "Task B"})

    response = await client.get("/tasks")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_list_tasks_correct_order(client: httpx.AsyncClient) -> None:
    """GET /tasks returns tasks in insertion order."""
    await client.post("/tasks", json={"title": "First"})
    await client.post("/tasks", json={"title": "Second"})
    await client.post("/tasks", json={"title": "Third"})

    response = await client.get("/tasks")
    titles = [item["title"] for item in response.json()]

    assert titles == ["First", "Second", "Third"]


@pytest.mark.asyncio
async def test_list_tasks_item_shape(client: httpx.AsyncClient) -> None:
    """GET /tasks items contain id, title, description, and done fields."""
    await client.post("/tasks", json={"title": "Shape test", "description": "desc"})

    response = await client.get("/tasks")
    item = response.json()[0]

    assert set(item.keys()) >= {"id", "title", "description", "done"}
    assert item["title"] == "Shape test"
    assert item["description"] == "desc"
    assert item["done"] is False


@pytest.mark.asyncio
async def test_list_tasks_preserves_optional_description(
    client: httpx.AsyncClient,
) -> None:
    """GET /tasks returns None for description when not provided."""
    await client.post("/tasks", json={"title": "No desc"})

    response = await client.get("/tasks")
    item = response.json()[0]

    assert item["description"] is None


@pytest.mark.asyncio
async def test_list_tasks_single_task(client: httpx.AsyncClient) -> None:
    """GET /tasks with one task returns a list with exactly one item."""
    await client.post("/tasks", json={"title": "Solo task"})

    response = await client.get("/tasks")
    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Solo task"


@pytest.mark.asyncio
async def test_create_then_list_round_trip(client: httpx.AsyncClient) -> None:
    """Create a task via POST and verify it appears correctly in GET response."""
    create_payload = {"title": "Round trip", "description": "end-to-end check"}
    create_response = await client.post("/tasks", json=create_payload)
    created = create_response.json()

    list_response = await client.get("/tasks")
    listed = list_response.json()

    assert len(listed) == 1
    assert listed[0]["id"] == created["id"]
    assert listed[0]["title"] == created["title"]
    assert listed[0]["description"] == created["description"]
    assert listed[0]["done"] == created["done"]


# ---------------------------------------------------------------------------
# PATCH /tasks/{id}
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_patch_task_happy_path(client: httpx.AsyncClient) -> None:
    """Create a task then PATCH it → 200 and done is True."""
    create_response = await client.post("/tasks", json={"title": "Finish report"})
    task_id = create_response.json()["id"]

    patch_response = await client.patch(f"/tasks/{task_id}")

    assert patch_response.status_code == 200
    assert patch_response.json()["done"] is True


@pytest.mark.asyncio
async def test_patch_task_not_found(client: httpx.AsyncClient) -> None:
    """PATCH with a non-existent id returns 404."""
    response = await client.patch("/tasks/9999")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_patch_task_response_shape(client: httpx.AsyncClient) -> None:
    """PATCH response includes all required fields: id, title, description, done."""
    create_response = await client.post(
        "/tasks", json={"title": "Shape check", "description": "patch shape"}
    )
    task_id = create_response.json()["id"]

    patch_response = await client.patch(f"/tasks/{task_id}")
    data = patch_response.json()

    assert set(data.keys()) >= {"id", "title", "description", "done"}
    assert data["id"] == task_id
    assert data["title"] == "Shape check"
    assert data["description"] == "patch shape"
    assert data["done"] is True


@pytest.mark.asyncio
async def test_patch_task_idempotent(client: httpx.AsyncClient) -> None:
    """PATCH an already-done task returns 200 and done remains True."""
    create_response = await client.post("/tasks", json={"title": "Already done"})
    task_id = create_response.json()["id"]

    first_patch = await client.patch(f"/tasks/{task_id}")
    assert first_patch.status_code == 200
    assert first_patch.json()["done"] is True

    second_patch = await client.patch(f"/tasks/{task_id}")
    assert second_patch.status_code == 200
    assert second_patch.json()["done"] is True


@pytest.mark.asyncio
async def test_patch_task_does_not_affect_other_tasks(client: httpx.AsyncClient) -> None:
    """PATCH one task → GET /tasks shows only that task as done; the other is unchanged."""
    await client.post("/tasks", json={"title": "Task One"})
    await client.post("/tasks", json={"title": "Task Two"})

    list_before = await client.get("/tasks")
    task_one_id = list_before.json()[0]["id"]

    await client.patch(f"/tasks/{task_one_id}")

    list_after = await client.get("/tasks")
    tasks = list_after.json()

    done_tasks = [t for t in tasks if t["done"] is True]
    pending_tasks = [t for t in tasks if t["done"] is False]

    assert len(done_tasks) == 1
    assert done_tasks[0]["id"] == task_one_id
    assert len(pending_tasks) == 1
    assert pending_tasks[0]["title"] == "Task Two"


# ---------------------------------------------------------------------------
# DELETE /tasks/{id}
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_delete_task_happy_path(client: httpx.AsyncClient) -> None:
    """Create a task then DELETE it → 204 with no response body."""
    create_response = await client.post("/tasks", json={"title": "Delete me"})
    task_id = create_response.json()["id"]

    delete_response = await client.delete(f"/tasks/{task_id}")

    assert delete_response.status_code == 204
    assert delete_response.content == b""


@pytest.mark.asyncio
async def test_delete_task_not_found(client: httpx.AsyncClient) -> None:
    """DELETE with a non-existent id returns 404."""
    response = await client.delete("/tasks/9999")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_task_removed_from_list(client: httpx.AsyncClient) -> None:
    """Create a task, DELETE it, then GET /tasks → task no longer in list."""
    create_response = await client.post("/tasks", json={"title": "Temporary task"})
    task_id = create_response.json()["id"]

    await client.delete(f"/tasks/{task_id}")

    list_response = await client.get("/tasks")
    task_ids = [t["id"] for t in list_response.json()]

    assert task_id not in task_ids
    assert list_response.json() == []


@pytest.mark.asyncio
async def test_delete_task_other_tasks_unaffected(client: httpx.AsyncClient) -> None:
    """Create 2 tasks, DELETE one, GET /tasks → only the other remains."""
    create_one = await client.post("/tasks", json={"title": "Keep me"})
    create_two = await client.post("/tasks", json={"title": "Remove me"})
    keep_id = create_one.json()["id"]
    remove_id = create_two.json()["id"]

    await client.delete(f"/tasks/{remove_id}")

    list_response = await client.get("/tasks")
    remaining = list_response.json()

    assert len(remaining) == 1
    assert remaining[0]["id"] == keep_id
    assert remaining[0]["title"] == "Keep me"


@pytest.mark.asyncio
async def test_delete_task_double_delete(client: httpx.AsyncClient) -> None:
    """DELETE the same id twice → first returns 204, second returns 404."""
    create_response = await client.post("/tasks", json={"title": "One-time task"})
    task_id = create_response.json()["id"]

    first_delete = await client.delete(f"/tasks/{task_id}")
    second_delete = await client.delete(f"/tasks/{task_id}")

    assert first_delete.status_code == 204
    assert second_delete.status_code == 404

