from fastapi import APIRouter
from src.database.utils import create_tables, drop_tables

db_router = APIRouter(tags=["database"])

@db_router.post("/setup_database")
async def setup_database():
    await drop_tables()
    await create_tables()
    return {"message": "Database setup complete"}

@db_router.post("/create_tables")
async def create_tables_endpoint():
    await create_tables()
    return {"message": "Tables created"}

@db_router.post("/drop_tables")
async def drop_tables_endpoint():
    await drop_tables()
    return {"message": "Tables dropped"}