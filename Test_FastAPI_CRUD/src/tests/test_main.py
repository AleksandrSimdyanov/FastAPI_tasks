import pytest
from fastapi import status


@pytest.mark.asyncio
def test_root_endpoint(client):
    """Тест корневого endpoint"""
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Task Manager API"


@pytest.mark.asyncio
def test_health_endpoint(client):
    """Тест health check"""
    response = client.get("/health")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "healthy"
    assert response.json()["database"] == "connected"


@pytest.mark.asyncio
def test_health_endpoint_after_operations(client):
    """Тест health check после операций с базой"""
    # Создаем задачу
    client.post("/tasks/", json={"title": "Health Test"})

    # Проверяем health
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "healthy"