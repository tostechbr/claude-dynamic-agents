import pytest
import pytest_asyncio
import httpx
from httpx import ASGITransport

import routers.tasks as tasks_module


@pytest_asyncio.fixture
async def client():
    from main import create_app

    app = create_app()
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(autouse=True)
def clear_tasks():
    """Clear the in-memory tasks list before each test to prevent interference."""
    tasks_module.tasks.clear()
    yield
    tasks_module.tasks.clear()
