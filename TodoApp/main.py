
from fastapi import  FastAPI
import models 
from TodoApp.databasesqlite import  engine
from routers import auth, todos, admin, user

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
app.include_router(todos.router, prefix="/api/v1", tags=["Todos"])
app.include_router(admin.router, prefix="/api/v1", tags=["Admin"])
app.include_router(user.router, prefix="/api/v1", tags=["User"])