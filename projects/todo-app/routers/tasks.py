from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.responses import Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import aiosqlite

from config import SECRET_KEY
from database import get_db
from schemas import Priority, TaskCreate, TaskResponse

router = APIRouter()
security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """Extract and validate JWT token from Authorization header.

    Returns user_id from token payload.
    Raises 401 HTTPException if token is invalid or missing.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token: missing user ID")
        return int(user_id)
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    except (ValueError, TypeError) as e:
        raise HTTPException(status_code=401, detail=f"Invalid user ID in token: {str(e)}")


@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(
    payload: TaskCreate,
    db: aiosqlite.Connection = Depends(get_db),
    current_user: int = Depends(get_current_user),
) -> TaskResponse:
    cursor = await db.execute(
        "INSERT INTO tasks (user_id, title, description, priority) VALUES (?, ?, ?, ?)",
        (current_user, payload.title, payload.description, payload.priority.value),
    )
    await db.commit()
    row = await db.execute(
        "SELECT id, title, description, done, priority FROM tasks WHERE id = ? AND user_id = ?",
        (cursor.lastrowid, current_user),
    )
    task = await row.fetchone()
    if task is None:
        raise HTTPException(status_code=500, detail="Failed to create task")
    return TaskResponse(
        id=task["id"],
        title=task["title"],
        description=task["description"],
        done=bool(task["done"]),
        priority=Priority(task["priority"]),
    )


@router.get("", response_model=list[TaskResponse])
async def list_tasks(
    db: aiosqlite.Connection = Depends(get_db),
    current_user: int = Depends(get_current_user),
) -> list[TaskResponse]:
    cursor = await db.execute(
        "SELECT id, title, description, done, priority FROM tasks WHERE user_id = ? ORDER BY id",
        (current_user,),
    )
    rows = await cursor.fetchall()
    return [
        TaskResponse(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            done=bool(row["done"]),
            priority=Priority(row["priority"]),
        )
        for row in rows
    ]


@router.patch("/{id}", response_model=TaskResponse)
async def mark_task_done(
    id: int = Path(gt=0),
    db: aiosqlite.Connection = Depends(get_db),
    current_user: int = Depends(get_current_user),
) -> TaskResponse:
    cursor = await db.execute(
        "SELECT id, title, description, done, priority FROM tasks WHERE id = ? AND user_id = ?",
        (id, current_user),
    )
    row = await cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.execute("UPDATE tasks SET done = 1 WHERE id = ? AND user_id = ?", (id, current_user))
    await db.commit()
    return TaskResponse(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        done=True,
        priority=Priority(row["priority"]),
    )


@router.delete("/{id}", status_code=204)
async def delete_task(
    id: int = Path(gt=0),
    db: aiosqlite.Connection = Depends(get_db),
    current_user: int = Depends(get_current_user),
) -> Response:
    cursor = await db.execute(
        "SELECT id FROM tasks WHERE id = ? AND user_id = ?", (id, current_user)
    )
    row = await cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (id, current_user))
    await db.commit()
    return Response(status_code=204)
