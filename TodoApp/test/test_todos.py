from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from routers.auth import get_current_user
from database import Base, get_db
from sqlalchemy.orm import sessionmaker
from main import app
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from models import Todos, User
from test_token import get_token_for_user
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/todos-app-test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def test_todos():
    db = TestSessionLocal()
    db.query(Todos).delete()  # Clear existing todos
    todos = [
        Todos(id=1,title="Test Todo 1", description="Description 1", priority=1, completed=False, owner_id=1),
        Todos(id=2,title="Test Todo 2", description="Description 2", priority=2, completed=True, owner_id=1)
    ]
    db.add_all(todos)
    db.commit()

def test_read_all_authenticated(test_todos):
    token = get_token_for_user()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/", headers=headers)
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "title": "Test Todo 1", "description": "Description 1", "priority": 1, "completed": False, "owner_id": 1},
        {"id": 2, "title": "Test Todo 2", "description": "Description 2", "priority": 2, "completed": True, "owner_id": 1}
    ]
def test_read_all_authenticated_admin(test_todos):
    token = get_token_for_user()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/todo", headers=headers)
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "title": "Test Todo 1",
            "description": "Description 1",
            "priority": 1,
            "completed": False,
            "owner_id": 1
        },
        {
            "id": 2,
            "title": "Test Todo 2",
            "description": "Description 2",
            "priority": 2,
            "completed": True,
            "owner_id": 1
        }
    ]