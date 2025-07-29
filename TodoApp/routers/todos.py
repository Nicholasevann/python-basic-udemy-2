from ast import Raise
from operator import gt, lt
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from models import Todos
from database import get_db
from .auth import get_current_user

router = APIRouter()


db_dependency = Annotated[Session, Depends(get_db)]
user_depedency = Annotated[dict,Depends(get_current_user)]
@router.get("/")
async def read_all(db: db_dependency, user:user_depedency):
    if user is None:
        return HTTPException(status_code=401, detail='Authentication Failed')
    todos = db.query(Todos).filter(Todos.owner_id == user.get('id')).all()
    return todos

@router.get("/todos/{todo_id}", status_code=200)
async def read_todo(todo_id: int, db: db_dependency, user:user_depedency):
    if user is None:
        return HTTPException(status_code=401, detail='Authentication Failed')
    todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo:
        return todo
    return {"message": "Todo not found"}

class TodoRequest(BaseModel):
    title: str = Field(min_length=3, example="Buy groceries")
    description: str = Field(min_length=5, example="Milk, Bread, Eggs")
    priority: int = Field(gt=0, lt=6, example=1)
    completed: bool = Field(..., example=False)

@router.post("/todos/", status_code=201)
async def create_todo(user:user_depedency,todo: TodoRequest, db: db_dependency):
    if user is None:
        return HTTPException(status_code=401, detail='Authentication Failed')
    db_todo = Todos(**todo.model_dump(), owner_id=user.get('id'))
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.put("/todos/{todo_id}", status_code=200)
async def update_todo(todo_id: int, todo: TodoRequest, db: db_dependency, user:user_depedency):
    if user is None:
        return HTTPException(status_code=401, detail='Authentication Failed')
    db_todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if not db_todo:
        return {"message": "Todo not found"}
    
    for key, value in todo.model_dump().items():
        setattr(db_todo, key, value)
    
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: str, db: db_dependency, user:user_depedency):
    if user is None:
        return HTTPException(status_code=401, detail='Authentication Failed')
    
    db_todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted successfully"}