from fastapi import APIRouter
from src.api.tasks import tasks_router
from src.api.setup_db import db_router


main_router = APIRouter()
main_router.include_router(tasks_router)
main_router.include_router(db_router)