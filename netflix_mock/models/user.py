from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from netflix_mock.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(String, unique=True, nullable=False)
    password_hash_key = Column(String, unique=True, nullable=False)
    salt = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    todos = relationship("netflix_mock.models.todo.Todo", back_populates="user")
