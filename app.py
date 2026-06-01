from fastapi import FastAPI,status,Response
from pydantic import BaseModel
from uuid import uuid4
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import json


app = FastAPI()


def tasks(filepath:str) -> list[dict]:
    try:
        with open(filepath,'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks:list[dict],filepath:str) -> None:
    with open(filepath,'w') as f:
        json.dump(tasks,f,indent=2,ensure_ascii=False)

tasks_db = tasks("tasks.json")

class Task(BaseModel):
    title: str
    done: bool = False 

class TaskNotFoundError(Exception):
    pass

@app.exception_handler(TaskNotFoundError)
def task_not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )

@app.get("/health")
def read() -> dict:
    return {"status":"ok"}

@app.get("/tasks")
def read_tasks() -> list[dict]:
    return tasks_db

@app.post("/tasks",status_code = 201)
def create_task(task: Task) -> JSONResponse:
    new_task = {"id": str(uuid4()),
        "title": task.title,
        "done": task.done}
    tasks_db.append(new_task)
    save_tasks(tasks_db, "tasks.json")
    
    return JSONResponse(
        content = new_task,
        status_code = 201,
        headers = {"Location":f"/tasks/{new_task['id']}"}
    )

@app.get("/tasks/{task_id}")
def read_task(task_id: str) -> dict:
        for task in tasks_db:
            if task["id"] == task_id:
                return task
        raise TaskNotFoundError("Task not found")
        

@app.put("/tasks/{task_id}")
def update_task(task_id: str, task: Task) -> dict:
    for t in tasks_db:
        if t["id"] == task_id:
            t["title"] = task.title
            t["done"] = task.done
            save_tasks(tasks_db, "tasks.json")
            return t   
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str)-> Response:
    for i,task in enumerate(tasks_db):
        if task["id"] == task_id:
            del tasks_db[i]
            save_tasks(tasks_db, "tasks.json")
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail="Task not found")
