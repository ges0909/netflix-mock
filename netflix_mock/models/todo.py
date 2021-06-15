from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from netflix_mock.database import Base


def resolve():
    from netflix_mock.models.user import User

    return User


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)

    text = Column(String, index=True)
    completed = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    user_id = Column(Integer, ForeignKey("users.id"))  # foreign key is table_name.column_name
    user = relationship("netflix_mock.models.user.User", back_populates="todos")
