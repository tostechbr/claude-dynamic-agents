import os
from collections.abc import AsyncGenerator

import aiosqlite

DB_PATH = os.path.join(os.path.dirname(__file__), "tasks.db")

CREATE_TASKS_TABLE = """
    CREATE TABLE IF NOT EXISTS tasks (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        title       TEXT    NOT NULL,
        description TEXT,
        done        INTEGER NOT NULL DEFAULT 0
    )
"""


async def init_db(db_path: str = DB_PATH) -> None:
    """Create the tasks table if it does not already exist."""
    async with aiosqlite.connect(db_path) as db:
        await db.execute(CREATE_TASKS_TABLE)
        await db.commit()


async def get_db() -> AsyncGenerator[aiosqlite.Connection, None]:
    """FastAPI dependency that yields an open aiosqlite connection."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        yield db
