from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.database.session import get_session
from src.database.requests import (
    create_task_request,
    get_task_request,
    get_tasks_request,
    update_task_request,
    delete_task_request
)
from src.schemas.tasks import TaskCreate, TaskUpdate, Task

tasks_router = APIRouter(prefix="/tasks", tags=["tasks"])

@tasks_router.post("/", response_model=Task)
async def create_task(task: TaskCreate, session: AsyncSession = Depends(get_session)):
    return await create_task_request(task, session)

@tasks_router.get("/", response_model=List[Task])
async def get_tasks(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)):
    return await get_tasks_request(session, skip, limit)

@tasks_router.get("/{task_uuid}", response_model=Task)
async def get_task(task_uuid: str, session: AsyncSession = Depends(get_session)):
    task = await get_task_request(task_uuid, session)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@tasks_router.put("/{task_uuid}", response_model=Task)
async def update_task(task_uuid: str, task_update: TaskUpdate, session: AsyncSession = Depends(get_session)):
    task = await update_task_request(task_uuid, task_update, session)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@tasks_router.delete("/{task_uuid}")
async def delete_task(task_uuid: str, session: AsyncSession = Depends(get_session)):
    success = await delete_task_request(task_uuid, session)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}