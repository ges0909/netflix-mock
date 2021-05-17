from sqlalchemy import Column, Integer, DateTime, func, String

from mock_server.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String)

    def __init__(
        self,
        username: str,
        hashed_password: str,
    ) -> None:
        super().__init__()
        self.username = username
        self.hashed_password = hashed_password
