from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)  # Remove this if using hashed_password
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")
    phone_number = Column(String, nullable=True)

    # Relationship to todos
    todos = relationship("Todos", back_populates="owner")

    def __repr__(self):
        return f"<User id={self.id} username={self.username}, role={self.role}>"


class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))

    # Relationship to user
    owner = relationship("User", back_populates="todos")

    def __repr__(self):
        return f"<Todo id={self.id} title={self.title} completed={self.completed}>"
