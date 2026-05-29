from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4
from fastapi import HTTPException

app = FastAPI()
tasks_db = []
class Task(BaseModel):
    title: str
    done: bool = False 


@app.get("/health")
def read():
    return {"status":"ok"}

@app.get("/tasks")
def read_tasks():
    return tasks_db

@app.post("/tasks")
def create_task(task: Task):
    new_task = {"id": str(uuid4()),
        "title": task.title,
        "done": task.done}
    tasks_db.append(new_task)
    return new_task

@app.get("/tasks/{task_id}")
def read_task(task_id: str):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}")
def update_task(task_id: str, task: Task):
    for t in tasks_db:
        if t["id"] == task_id:
            t["title"] = task.title
            t["done"] = task.done
            return t
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    for i,task in enumerate(tasks_db):
        if task["id"] == task_id:
            del tasks_db[i]
            return {"detail": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
