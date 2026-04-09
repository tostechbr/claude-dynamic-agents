from fastapi import APIRouter, HTTPException

from schemas import TaskCreate, TaskResponse

router = APIRouter()

tasks: list[dict] = []


@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(payload: TaskCreate) -> TaskResponse:
    task = {
        "id": len(tasks) + 1,
        "title": payload.title,
        "description": payload.description,
        "done": False,
    }
    tasks.append(task)
    return TaskResponse(**task)


@router.get("", response_model=list[TaskResponse])
async def list_tasks() -> list[TaskResponse]:
    return [TaskResponse(**task) for task in tasks]


@router.patch("/{id}", response_model=TaskResponse)
async def mark_task_done(id: int) -> TaskResponse:
    for task in tasks:
        if task["id"] == id:
            updated = {**task, "done": True}
            tasks[tasks.index(task)] = updated
            return TaskResponse(**updated)
    raise HTTPException(status_code=404, detail="Task not found")
