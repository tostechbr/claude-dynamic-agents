from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response

import aiosqlite

from database import get_db
from schemas import TaskCreate, TaskResponse

router = APIRouter()


@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(
    payload: TaskCreate,
    db: aiosqlite.Connection = Depends(get_db),
) -> TaskResponse:
    cursor = await db.execute(
        "INSERT INTO tasks (title, description) VALUES (?, ?)",
        (payload.title, payload.description),
    )
    await db.commit()
    row = await db.execute(
        "SELECT id, title, description, done FROM tasks WHERE id = ?",
        (cursor.lastrowid,),
    )
    task = await row.fetchone()
    return TaskResponse(
        id=task["id"],
        title=task["title"],
        description=task["description"],
        done=bool(task["done"]),
    )


@router.get("", response_model=list[TaskResponse])
async def list_tasks(
    db: aiosqlite.Connection = Depends(get_db),
) -> list[TaskResponse]:
    cursor = await db.execute(
        "SELECT id, title, description, done FROM tasks ORDER BY id"
    )
    rows = await cursor.fetchall()
    return [
        TaskResponse(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            done=bool(row["done"]),
        )
        for row in rows
    ]


@router.patch("/{id}", response_model=TaskResponse)
async def mark_task_done(
    id: int,
    db: aiosqlite.Connection = Depends(get_db),
) -> TaskResponse:
    await db.execute("UPDATE tasks SET done = 1 WHERE id = ?", (id,))
    await db.commit()
    cursor = await db.execute(
        "SELECT id, title, description, done FROM tasks WHERE id = ?", (id,)
    )
    row = await cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        done=bool(row["done"]),
    )


@router.delete("/{id}", status_code=204)
async def delete_task(
    id: int,
    db: aiosqlite.Connection = Depends(get_db),
) -> Response:
    cursor = await db.execute("SELECT id FROM tasks WHERE id = ?", (id,))
    row = await cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.execute("DELETE FROM tasks WHERE id = ?", (id,))
    await db.commit()
    return Response(status_code=204)
