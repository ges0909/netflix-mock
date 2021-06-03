from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func

from netflix_mock.common.database import Base
from netflix_mock.schemas.todo import TodoCreate


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)

    text = Column(String, index=True)
    completed = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    user_id = Column(Integer, ForeignKey("users.id"))

    def __init__(self, todo: TodoCreate):
        super().__init__()
        self.text = todo.text
        self.completed = todo.completed
