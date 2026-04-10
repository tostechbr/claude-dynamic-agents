from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Priority = Priority.medium


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    done: bool
    priority: Priority
