from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from netflix_mock.common.database import Base
from netflix_mock.schemas.user import UserCreate


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(String, unique=True, nullable=False)
    password = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    todos = relationship("Todo", back_populates="owner", cascade="all, delete-orphan")

    def __init__(self, user: UserCreate):
        super().__init__()
        self.username = user.username
        self.password = user.password.get_secret_value() + "_not_really_hashed"
        self.email = user.email
        self.first_name = user.first_name
        self.last_name = user.last_name
