---
name: fastapi-patterns
description: "Use when building or reviewing FastAPI backends: routers, dependency injection, Pydantic models, async patterns, authentication, middleware"
---

# FastAPI Patterns

## Project Structure

```
app/
├── main.py              ← app factory, middleware, lifespan
├── api/
│   ├── deps.py          ← shared dependencies (db, auth)
│   └── v1/
│       ├── router.py    ← includes all sub-routers
│       └── endpoints/
│           ├── auth.py
│           └── users.py
├── core/
│   ├── config.py        ← Settings via pydantic-settings
│   └── security.py      ← password hashing, JWT
├── models/
│   └── user.py          ← SQLAlchemy models
├── schemas/
│   └── user.py          ← Pydantic request/response schemas
└── services/
    └── user_service.py  ← business logic (no DB calls here)
```

## App Factory Pattern

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await db.connect()
    yield
    # shutdown
    await db.disconnect()

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(api_router, prefix="/api/v1")
    return app
```

## Dependency Injection

```python
# deps.py — reusable dependencies
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(
    token: str = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    payload = verify_token(token.credentials)
    user = await db.get(User, payload["sub"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Usage in endpoint
@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return user
```

## Pydantic Schemas

```python
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}
```

## Async Database (SQLAlchemy 2.0)

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(settings.DATABASE_URL)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSession(engine) as session:
        yield session
```

## Error Handling

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message}
    )
```

## Key Principles

- Use `Depends()` for all shared state — never use globals
- Schemas (Pydantic) and Models (SQLAlchemy) are separate — never mix
- Business logic lives in `services/`, not in endpoints
- Always use `async def` for endpoints that do I/O
- Validate at schema level, not in endpoint logic
- Return typed responses — always define a `response_model`
