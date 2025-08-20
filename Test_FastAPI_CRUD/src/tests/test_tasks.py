import pytest
from fastapi import status


@pytest.mark.asyncio
def test_create_task(client):
    """Тест создания задачи"""
    response = client.post("/tasks/", json={
        "title": "Test Task",
        "description": "Test Description",
        "status": "created"
    })

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["status"] == "created"
    assert "uuid" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
def test_create_task_minimal_data(client):
    """Тест создания задачи с минимальными данными"""
    response = client.post("/tasks/", json={
        "title": "Minimal Task"
    })

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Minimal Task"
    assert data["description"] is None
    assert data["status"] == "created"


@pytest.mark.asyncio
def test_get_tasks_empty(client):
    """Тест получения пустого списка задач"""
    response = client.get("/tasks/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.asyncio
def test_get_tasks_with_data(client):
    """Тест получения списка задач с данными"""
    # Создаем задачу
    client.post("/tasks/", json={
        "title": "Test Task 1",
        "description": "Description 1"
    })

    # Получаем список задач
    response = client.get("/tasks/")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Task 1"
    assert data[0]["description"] == "Description 1"


@pytest.mark.asyncio
def test_get_task_by_uuid(client):
    """Тест получения задачи по UUID"""
    # Создаем задачу
    create_response = client.post("/tasks/", json={
        "title": "Specific Task",
        "description": "Specific Description"
    })
    task_uuid = create_response.json()["uuid"]

    # Получаем задачу по UUID
    response = client.get(f"/tasks/{task_uuid}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Specific Task"
    assert data["uuid"] == task_uuid


@pytest.mark.asyncio
def test_get_nonexistent_task(client):
    """Тест получения несуществующей задачи"""
    response = client.get("/tasks/nonexistent-uuid-123")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Task not found"


@pytest.mark.asyncio
def test_update_task(client):
    """Тест обновления задачи"""
    # Создаем задачу
    create_response = client.post("/tasks/", json={
        "title": "Original Title",
        "description": "Original Description",
        "status": "created"
    })
    task_uuid = create_response.json()["uuid"]

    # Обновляем задачу
    update_response = client.put(f"/tasks/{task_uuid}", json={
        "title": "Updated Title",
        "status": "in_progress"
    })

    assert update_response.status_code == status.HTTP_200_OK
    data = update_response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Original Description"
    assert data["status"] == "in_progress"


@pytest.mark.asyncio
def test_update_nonexistent_task(client):
    """Тест обновления несуществующей задачи"""
    response = client.put("/tasks/nonexistent-uuid-123", json={
        "title": "Updated Title"
    })

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Task not found"


@pytest.mark.asyncio
def test_delete_task(client):
    """Тест удаления задачи"""
    # Создаем задачу
    create_response = client.post("/tasks/", json={
        "title": "Task to delete"
    })
    task_uuid = create_response.json()["uuid"]

    # Удаляем задачу
    delete_response = client.delete(f"/tasks/{task_uuid}")

    assert delete_response.status_code == status.HTTP_200_OK
    assert delete_response.json()["message"] == "Task deleted"

    # Проверяем, что задача удалена
    get_response = client.get(f"/tasks/{task_uuid}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
def test_delete_nonexistent_task(client):
    """Тест удаления несуществующей задачи"""
    response = client.delete("/tasks/nonexistent-uuid-123")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Task not found"


@pytest.mark.asyncio
def test_pagination(client):
    """Тест пагинации"""
    # Создаем несколько задач
    for i in range(5):
        client.post("/tasks/", json={
            "title": f"Task {i + 1}",
            "description": f"Description {i + 1}"
        })

    # Получаем первые 2 задачи
    response = client.get("/tasks/?skip=0&limit=2")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2

    # Получаем следующие 2 задачи
    response = client.get("/tasks/?skip=2&limit=2")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2

    # Получаем оставшиеся задачи
    response = client.get("/tasks/?skip=4&limit=10")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1