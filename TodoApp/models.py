from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Todo id={self.id} title={self.title} completed={self.completed}>"