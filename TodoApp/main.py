
from fastapi import  FastAPI
import models 
from database import  engine
from routers import auth, todos

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
app.include_router(todos.router, prefix="/api/v1", tags=["Todos"])