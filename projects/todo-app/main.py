from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.tasks import router as tasks_router

ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


def create_app() -> FastAPI:
    app = FastAPI(title="Todo App", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
    return app


app = create_app()
