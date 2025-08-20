import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from main import app
from src.database.session import get_session

# Тестовая база в памяти
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)


async def override_get_session():
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture(scope="session")
def event_loop():
    """Создаем event loop для тестов"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    """Создаем и удаляем таблицы для каждого теста"""
    # Создаем таблицы
    async with test_engine.begin() as conn:
        from src.database.models import Base
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Удаляем таблицы
    async with test_engine.begin() as conn:
        from src.database.models import Base
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
def client():
    """Создаем тестового клиента"""
    # Переопределяем зависимость сессии
    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as test_client:
        yield test_client

    # Очищаем переопределения
    app.dependency_overrides.clear()