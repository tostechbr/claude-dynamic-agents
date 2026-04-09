from fastapi import FastAPI

from routers.tasks import router as tasks_router


def create_app() -> FastAPI:
    app = FastAPI(title="Todo App", version="0.1.0")
    app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
    return app


app = create_app()
