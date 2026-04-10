from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)
    priority: Priority = Priority.medium


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    done: bool
    priority: Priority
