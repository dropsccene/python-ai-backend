from fastapi.testclient import TestClient
from app import app
from fastapi import Response
from fastapi.responses import JSONResponse

client = TestClient(app)

def test_read():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status":"ok"}

def test_not_found():
    response = client.get("/nonexistent")
    assert response.status_code == 404

def test_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []

def test_create_tasks():
    response = client.post("/tasks", json={"title": "Test Task"})
    assert response.status_code == 201
    

def test_read_tasks():
    create_resp = client.post("/tasks",json={"title":"独立测试任务"})
    task_id = create_resp.json()["id"]
    resp = client.get(f"/tasks/{task_id}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "独立测试任务"

def test_not_tasks_found():
    response = client.get("/tasks/nonexistent")
    assert response.status_code == 404

def test_update_tasks():
    response = client.get(f"/tasks")
    task_id = response.json()[0]["id"]
    response = client.put(f"/tasks/{task_id}", json={"title": "更新后的任务", "done": True})
    assert response.status_code == 200
    assert response.json()["done"] == True

def test_not_found_update():
    response = client.put("/tasks/{task_id}/nonexistent",json={"title": "更新后的任务", "done": True})
    assert response.status_code == 404

def test_delete_tasks():
    response = client.get("/tasks")
    task_id = response.json()[0]["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

def test_not_found_delete():
    response = client.delete("/tasks/nonexistent")
    assert response.status_code == 404