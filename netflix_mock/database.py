from typing import Optional, Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import sessionmaker, Session


# async: https://docs.sqlalchemy.org/en/14/_modules/examples/asyncio/async_orm.html
from netflix_mock.config import Config

Base = declarative_base()


class Database:
    def __init__(self):
        config = Config()
        self._engine = create_engine(
            url=config.database_url,
            echo=config.database_logging,
            connect_args={"check_same_thread": False},  # for SQLite only
        )
        # create session factory
        self._session_maker = sessionmaker(
            # autocommit=False,
            # autoflush=False,
            bind=self._engine,
        )
        # generate model schemas
        with self._engine.begin() as conn:
            # Base.metadata.drop_all(conn)
            Base.metadata.create_all(conn)

    @property
    def session_maker(self):
        return self._session_maker


_database: Optional[Database] = None


def get_db_session() -> Iterator[Session]:
    global _database
    if not _database:
        _database = Database()
    with _database.session_maker() as session:  # 'session_maker' is called
        yield session
        # session is closed automatically by context manager
