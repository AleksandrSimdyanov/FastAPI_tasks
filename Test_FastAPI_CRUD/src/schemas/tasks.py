from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "created"


class TaskCreate(TaskBase):
    uuid: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class Task(TaskBase):
    uuid: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True