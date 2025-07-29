from typing import Annotated
from fastapi import  APIRouter, HTTPException
from pydantic import BaseModel
from models import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from database import get_db
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer,HTTPAuthorizationCredentials
from jose import jwt, JWTError
router = APIRouter(
)
SECRET_KEY = "77646f65c770e0641965a9c818b2665192b3e69e467b45a0f53dcf9297e6e7c3"
ALGORITHM = "HS256"
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = HTTPBearer()
class CreateUserRequest(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    password:str
    role:str
    phone_number: str | None = None

db_dependency = Annotated[Session, Depends(get_db)]
@router.post("/auth/", status_code=201)
async def create_user(db:db_dependency,create_user_request: CreateUserRequest):
    create_user_model = User(
        username=create_user_request.username,
        password=create_user_request.password,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
        phone_number=create_user_request.phone_number
    )
    db.add(create_user_model)
    db.commit()
    return create_user_model

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    print(user)
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.get("/token/")
async def get_current_user(token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return {"username": username, "id": user_id,'user_role':user_role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Unauthorized")
@router.post("/token", status_code=200)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) 
    token = create_access_token(data={"sub": user.username, "id": user.id,"role":user.role})
    return {"access_token": token, "token_type": "bearer"}

