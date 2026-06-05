from fastapi import FastAPI,status,Response,Depends
from pydantic import BaseModel
from uuid import uuid4
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import json
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from models import User,Article
from schemas import UserCreate,ArticleCreate

app = FastAPI()

@app.get("/users")
def get_users(db : Session = Depends(get_db)):
	user = db.query(User).all()
	return user

@app.post("/users")
def create_user(user_data : UserCreate,db : Session = Depends(get_db)):
    user = User(**user_data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get("/users/{user_id:int}")
def get_user(user_id :int ,db : Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id:int}")
def update_user(user_id : int, user_data : UserCreate,db : Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.username = user_data.username
    user.email = user_data.email
    db.commit()
    db.refresh(user)
    return user


@app.delete("/users/{user_id:int}")
def delete_user(user_id:int,db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/articles")
def get_articles(db : Session = Depends(get_db)):
	articles = db.query(Article).all()
	return articles

@app.get("/articles/{article_id}")
def get_article(article_id:int,db:Session = Depends(get_db)):
	article = db.query(Article).filter(Article.id == article_id).first()
	if article is None:
		raise HTTPException(status = 404,detail="Article not found")
	return article

@app.post("/users/{user_id:int}/articles")
def create_articles(user_id:int,user_data:ArticleCreate,db :Session = Depends(get_db)):
	article = Article(**user_data.model_dump(),user_id = user_id)
	db.add(article)
	db.commit()
	db.refresh(article)
	return article

@app.get("/test-db")
def test_db(db :Session = Depends(get_db)):
    return {"working" : db is not None}

@app.get("/ping-db")
def check_connection(session:Session = Depends(get_db)):
    try:
        session.execute(text("SELECT 1"))
        return {"database" : "connected"}
    except Exception as e:
        return {"database" : "error", "details": str(e)}

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
