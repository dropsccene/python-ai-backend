import httpx

r = httpx.get("http://localhost:8000/health")
r.status_code
r.json()
print(r.status_code)
print(r.json())

r = httpx.post("http://localhost:8000/tasks",json={"title":"测试任务","done":False})
r.status_code
r.json()
print(r.status_code)
print(r.json())

r = httpx.get("http://localhost:8000/tasks")
r.status_code
r.json()
print(r.status_code)
print(r.json())

# 先创建
create_resp = httpx.post("http://localhost:8000/tasks",json={"title":"独立测试任务"})
# 获取ID
task_id = create_resp.json()["id"]

r = httpx.put(f"http://localhost:8000/tasks/{task_id}", json={"title": "更新后的任务", "done": True})
r.status_code
r.json()
print(r.status_code)
print(r.json())

r = httpx.delete(f"http://localhost:8000/tasks/{task_id}")
r.status_code
r.json()
print(r.status_code)
print(r.json())