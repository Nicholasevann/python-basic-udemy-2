from http import client
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from routers.auth import authenticate_user, get_current_user
from database import Base, get_db
from sqlalchemy.orm import sessionmaker
from main import app
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from models import Todos, User
from passlib.context import CryptContext
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/todos-app-test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

client = TestClient(app)



def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def test_user():
    db = TestSessionLocal()
    db.query(Todos).delete()
    db.query(User).delete()
    user = User(
        username="testuser",
        first_name="Test",
        last_name="User",
        role="admin",
        hashed_password=bcrypt_context.hash("testpassword"),
        is_active=True,
        id=1,
    )
    db.add(user)
    db.commit()
    yield user

def test_authenticate_user(test_user):
    db = TestSessionLocal()
    user = authenticate_user(db, "testuser", "testpassword")
    assert user is not False
    assert user.username == "testuser"

def get_token_for_user(username="testuser", password="testpassword"):
    response = client.post(
        "/api/v1/token",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]