import pytest
import pytest_asyncio
import aiosqlite
import httpx
from httpx import ASGITransport

from database import get_db, CREATE_TASKS_TABLE


@pytest_asyncio.fixture
async def db() -> aiosqlite.Connection:
    """In-memory SQLite connection with tasks table for test isolation."""
    async with aiosqlite.connect(":memory:") as conn:
        conn.row_factory = aiosqlite.Row
        await conn.execute(CREATE_TASKS_TABLE)
        await conn.commit()
        yield conn


@pytest_asyncio.fixture
async def client(db: aiosqlite.Connection) -> httpx.AsyncClient:
    from main import create_app

    app = create_app()

    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
