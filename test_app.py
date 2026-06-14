from fastapi.testclient import TestClient
import os
os.environ["SECRET"] = "test-secret"
import app
from fastapi import Response
from fastapi.responses import JSONResponse
import pytest
from sqlalchemy.orm import Session
from database import engine
from models import User,Article,Tag,article_tags,Tag
import json
import jwt
from datetime import datetime, timedelta,timezone

SECRET_KEY = "test-secret"
ALGORITHM = "HS256"

def create_test_token(user_id:int = 1)->str:
	payload = {
		"sub" : str(user_id),
		"exp": datetime.now(timezone.utc) + timedelta(hours=1)
	}
	return jwt.encode(payload,SECRET_KEY,algorithm = ALGORITHM)


client = TestClient(app.app)

@pytest.fixture(autouse=True)
def setup():
    app.tasks_db.clear()
    with open("tasks.json", "w") as f:
        f.write("[]")
    session = Session(engine)
    session.query(article_tags).delete()
    session.query(Article).delete()
    session.query(Tag).delete()
    session.query(User).delete()
    session.commit()
    session.close()



def test_user():
    response = client.post("/users",json={"username":"测试用户","email":"test@test.com","password":"test123"})
    user_id = response.json()["id"]
    token = create_test_token(user_id)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/users", headers=headers)
    assert response.status_code == 200
    assert response.json() == [{"id":user_id,"username":"测试用户","email":"test@test.com"}]

def test_create_user():
    response = client.post(f"/users", json={"username":"测试用户","email":"test@test.com","password":"test123"})
    user_id = response.json()["id"]
    token = create_test_token(user_id)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/users/{user_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "测试用户"

def test_get_user():
    create_resp = client.post("/users",json={"username":"测试用户2","email":"test2@test.com","password":"test123"})
    user_id = create_resp.json()["id"]
    token = create_test_token(user_id)
    headers = {"Authorization":f"Bearer {token}"}
    response = client.get(f"/users/{user_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "test2@test.com"

def test_update_user():
    create_resp = client.post("/users",json={"username":"测试用户3","email":"test3@test.com","password":"test456"})
    user_id = create_resp.json()["id"]
    token = create_test_token(user_id)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(f"/users/{user_id}",headers=headers,json={"username":"更新用户3","email":"updated@test.com","password":"updated123"})
    assert response.status_code == 200
    assert response.json()["username"] == "更新用户3"

def test_delete_user():
    create_resp = client.post("/users",json={"username":"测试用户4","email":"test4@test.com","password":"test123"})
    user_id = create_resp.json()["id"]
    token = create_test_token(user_id)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(f"/users/{user_id}",headers=headers)
    assert response.status_code == 204

def test_not_found1():
	response =client.post("/users",json={"username":"测试用户","email":"test@test.com","password":"test123"})
	user_id = response.json()["id"]
	token = create_test_token(user_id)
	headers = {"Authorization": f"Bearer {token}"}
	response = client.get(f"/users/999999", headers=headers)
	assert response.status_code == 404


def test_not_found2():
	response = client.get(f"/users")
	assert response.status_code == 401

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
    # 首先创建一个任务
    create_resp = client.post("/tasks",json={"title":"待更新任务"})
    task_id = create_resp.json()["id"]
    # 然后更新这个任务
    response = client.put(f"/tasks/{task_id}", json={"title": "更新后的任务", "done": True})
    # 断言
    assert response.status_code == 200
    assert response.json()["done"] == True

def test_not_found_update():
    response = client.put("/tasks/nonexistent",json={"title": "更新后的任务", "done": True})
    assert response.status_code == 404

def test_delete_tasks():
    create_resp = client.post("/tasks",json={"title":"待删除任务"})
    task_id = create_resp.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

def test_not_found_delete():
    response = client.delete("/tasks/nonexistent")
    assert response.status_code == 404