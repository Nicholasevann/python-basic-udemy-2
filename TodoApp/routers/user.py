from ast import Raise
from operator import gt, lt
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from models import Todos,User
from TodoApp.databasesqlite import SessionLocal, engine
from .auth import get_current_user
from passlib.context import CryptContext
router = APIRouter(
    prefix="/user",
    tags=['user']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_depedency = Annotated[dict,Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserVerification(BaseModel):
    password:str
    mew_password:str = Field(min_length=6, example="new_password123")

@router.get("/", status_code=200)
async def read_all_users(db: db_dependency, user:user_depedency):
    print(user)
    if user is None :
        raise HTTPException(status_code=401, detail="Authenticated Failed")
    users = db.query(User).filter(User.id == user.get('id')).first()
    return users 

@router.put("/update-password", status_code=200)
async def update_password(user:user_depedency, user_verification: UserVerification, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authenticated Failed")
    user_model = db.query(User).filter(User.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    user_model.hashed_password = bcrypt_context.hash(user_verification.mew_password)
    db.add(user_model)
    db.commit()
    