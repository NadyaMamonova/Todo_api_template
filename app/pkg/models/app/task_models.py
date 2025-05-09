from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import validator, Field
from uuid import uuid4
from app.pkg.models.base.model import BaseModel

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    ARCHIVED = "archived"

class TaskFields:
    id: str = "id"
    title: str = "title"
    description: str = "description"
    created_at: str = "created_at"
    due_date: str = "due_date"
    status: str = "status"


class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))  # Генерация UUID как строки
    title: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    due_date: Optional[datetime] = None
    status: TaskStatus = TaskStatus.TODO

    @validator('id', pre=True)
    def validate_id(cls, v):
        if v is None:
            return str(uuid4())
        return str(v)
