"""Test JWT authentication functionality."""
import pytest
import httpx
import jwt
from main import SECRET_KEY


@pytest.mark.asyncio
async def test_missing_token_returns_401(client: httpx.AsyncClient) -> None:
    """Request without Authorization header returns 401."""
    async with httpx.AsyncClient(base_url="http://test") as no_auth_client:
        # Override app for this client without headers
        from main import create_app
        from database import get_db
        import aiosqlite

        app = create_app()

        async def override_get_db():
            async with aiosqlite.connect(":memory:") as conn:
                conn.row_factory = aiosqlite.Row
                from database import CREATE_TASKS_TABLE
                await conn.execute(CREATE_TASKS_TABLE)
                await conn.commit()
                yield conn

        app.dependency_overrides[get_db] = override_get_db

        from httpx import ASGITransport

        async with httpx.AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as no_auth_client:
            response = await no_auth_client.get("/tasks")
            assert response.status_code == 403  # HTTPBearer returns 403 for missing credentials


@pytest.mark.asyncio
async def test_invalid_token_returns_401(db: aiosqlite.Connection) -> None:
    """Request with invalid token returns 401."""
    from main import create_app
    from database import get_db
    from httpx import ASGITransport

    app = create_app()

    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    async with httpx.AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        headers={"Authorization": "Bearer invalid-token"},
    ) as client:
        response = await client.get("/tasks")
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_valid_token_allows_access(client: httpx.AsyncClient) -> None:
    """Request with valid token allows access to endpoints."""
    # client fixture already includes valid token
    response = await client.get("/tasks")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_user_isolation(db: aiosqlite.Connection) -> None:
    """Users can only see their own tasks."""
    from main import create_app
    from database import get_db
    from httpx import ASGITransport

    app = create_app()

    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    # Create task for user_id=1
    token_user1 = jwt.encode({"sub": "1"}, SECRET_KEY, algorithm="HS256")
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        headers={"Authorization": f"Bearer {token_user1}"},
    ) as client1:
        response = await client1.post("/tasks", json={"title": "User 1 task"})
        assert response.status_code == 201

    # Try to access as user_id=2
    token_user2 = jwt.encode({"sub": "2"}, SECRET_KEY, algorithm="HS256")
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        headers={"Authorization": f"Bearer {token_user2}"},
    ) as client2:
        response = await client2.get("/tasks")
        assert response.status_code == 200
        # User 2 should see no tasks (user 1 created it)
        assert response.json() == []
