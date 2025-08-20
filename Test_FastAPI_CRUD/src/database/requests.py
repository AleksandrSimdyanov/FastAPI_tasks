from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List
from src.database.models import Task


async def create_task_request(task_data, session: AsyncSession):
    new_task = Task(
        uuid=str(task_data.uuid) if hasattr(task_data, 'uuid') else None,
        title=task_data.title,
        description=task_data.description,
        status=task_data.status
    )
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    return new_task


async def get_task_request(task_uuid: str, session: AsyncSession):
    result = await session.execute(select(Task).where(Task.uuid == task_uuid))
    return result.scalar_one_or_none()


async def get_tasks_request(session: AsyncSession, skip: int = 0, limit: int = 100):
    result = await session.execute(select(Task).offset(skip).limit(limit))
    return result.scalars().all()


async def update_task_request(task_uuid: str, task_update, session: AsyncSession):
    task = await get_task_request(task_uuid, session)
    if not task:
        return None

    if task_update.title:
        task.title = task_update.title
    if task_update.description:
        task.description = task_update.description
    if task_update.status:
        task.status = task_update.status

    await session.commit()
    await session.refresh(task)
    return task


async def delete_task_request(task_uuid: str, session: AsyncSession):
    task = await get_task_request(task_uuid, session)
    if not task:
        return False

    await session.delete(task)
    await session.commit()
    return True