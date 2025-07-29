from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from TodoApp.databasesqlite import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")

    def __repr__(self):
        return f"<User id={self.id} username={self.username}, role={self.role}>"
class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return f"<Todo id={self.id} title={self.title} completed={self.completed}>"