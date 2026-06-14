from fastapi import FastAPI,status,Response,Depends
from pydantic import BaseModel
from uuid import uuid4
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import json
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from models import User,Article,Tag
from schemas import UserCreate,ArticleCreate,TagCreate
import bcrypt
from schemas import UserResponse,ArticleResponse,TagResponse
import jwt
import datetime
import secrets
from fastapi.security import OAuth2PasswordBearer
import os





oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


app = FastAPI()

SECRET = os.getenv("SECRET",secrets.token_hex(32))


@app.get("/users/{id:int}")
def get_user(id:int,db:Session= Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user).model_dump()

@app.get("/articles/{id:int}")
def get_article(id:int,db:Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return ArticleResponse.model_validate(article).model_dump()

@app.post("/register",response_model = UserResponse)
def create_register(user:UserCreate,db:Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    pwd_hash = bcrypt.hashpw(user.password.encode(),bcrypt.gensalt())
    db_user = User(username = user.username,email = user.email,password = pwd_hash.decode())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login")
def login(form:UserCreate,db:Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == form.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not bcrypt.checkpw(form.password.encode(),db_user.password.encode()):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = jwt.encode({"username":db_user.username,"sub":str(db_user.id),"exp":datetime.datetime.utcnow() + datetime.timedelta(hours=2)},SECRET,algorithm="HS256")
    return {"access_token":token,"token_type":"bearer","expires_in":7200}

def get_current_user(token:str = Depends(oauth2_scheme),db:Session = Depends(get_db)):
    try:
        payload = jwt.decode(token,SECRET,algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id == int(payload.get("sub"))).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.get("/users",response_model = list[UserResponse])
def get_users(db:Session = Depends(get_db),current_user:User = Depends(get_current_user)):
    users = db.query(User).all()
    return users

@app.get("/users/me",response_model = UserResponse)
def get_me(current_user:User = Depends(get_current_user)):
    return current_user

@app.post("/tags")
def create_tag(tag_data : TagCreate,db : Session = Depends(get_db)):
    tag = Tag(**tag_data.model_dump())
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

@app.get("/tags")
def get_tags(db : Session = Depends(get_db)):
    tags = db.query(Tag).all()
    return tags

@app.post("/articles/{article_id}/tags/{tag_id}")
def add_tag_to_article(article_id:int,tag_id:int,db:Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    article.tags.append(tag)
    db.commit()
    return {"OK":True}

@app.get("/users")
def get_users(db : Session = Depends(get_db),current_user:User = Depends(get_current_user)):
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
        raise HTTPException(status_code=404, detail="Article not found")
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
