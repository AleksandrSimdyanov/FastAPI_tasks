import pytest
from fastapi import status


@pytest.mark.asyncio
def test_setup_database(client):
    """Тест пересоздания базы данных"""
    response = client.post("/setup_database")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Database setup complete"


@pytest.mark.asyncio
def test_create_tables(client):
    """Тест создания таблиц"""
    response = client.post("/create_tables")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Tables created"


@pytest.mark.asyncio
def test_drop_tables(client):
    """Тест удаления таблиц"""
    response = client.post("/drop_tables")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Tables dropped"


@pytest.mark.asyncio
def test_database_operations_flow(client):
    """Тест полного цикла работы с базой"""
    # Удаляем таблицы
    drop_response = client.post("/drop_tables")
    assert drop_response.status_code == status.HTTP_200_OK

    # Создаем таблицы
    create_response = client.post("/create_tables")
    assert create_response.status_code == status.HTTP_200_OK

    # Проверяем, что можно работать с базой
    task_response = client.post("/tasks/", json={"title": "Test Task"})
    assert task_response.status_code == status.HTTP_200_OK

    # Полный reset
    setup_response = client.post("/setup_database")
    assert setup_response.status_code == status.HTTP_200_OK

    # После reset база должна быть пустой
    tasks_response = client.get("/tasks/")
    assert tasks_response.status_code == status.HTTP_200_OK
    assert tasks_response.json() == []