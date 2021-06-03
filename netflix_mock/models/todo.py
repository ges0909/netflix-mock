from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from netflix_mock.database import Base
from netflix_mock.schemas.todo import TodoCreate


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)

    text = Column(String, index=True)
    completed = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    user_id = Column(Integer, ForeignKey("users.id"))  # foreign key has to be table_name.column_name

    user = relationship(
        "netflix_mock.models.User",
        back_populates="todos",  # relation 'todos'
    )

    def __init__(self, todo: TodoCreate):
        super().__init__()
        self.text = todo.text
        self.completed = todo.completed
