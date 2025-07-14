from ast import Raise
from operator import gt, lt
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
import models 
from models import Todos
from database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
@app.get("/")
async def read_all(db: db_dependency):
    todos = db.query(models.Todos).all()
    return todos

@app.get("/todos/{todo_id}", status_code=200)
async def read_todo(todo_id: int, db: db_dependency):
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo:
        return todo
    return {"message": "Todo not found"}

class TodoRequest(BaseModel):
    title: str = Field(min_length=3, example="Buy groceries")
    description: str = Field(min_length=5, example="Milk, Bread, Eggs")
    priority: int = Field(gt=0, lt=6, example=1)
    completed: bool = Field(..., example=False)

@app.post("/todos/", status_code=201)
async def create_todo(todo: TodoRequest, db: db_dependency):
    db_todo = models.Todos(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.put("/todos/{todo_id}", status_code=200)
async def update_todo(todo_id: int, todo: TodoRequest, db: db_dependency):
    db_todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if not db_todo:
        return {"message": "Todo not found"}
    
    for key, value in todo.model_dump().items():
        setattr(db_todo, key, value)
    
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: str, db: db_dependency):
    db_todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted successfully"}