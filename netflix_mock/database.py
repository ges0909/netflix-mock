from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import sessionmaker

from netflix_mock.config import get_settings, Settings

# async: https://docs.sqlalchemy.org/en/14/_modules/examples/asyncio/async_orm.html

Base = declarative_base()


class Database:
    def __init__(self, settings: Settings):
        self.engine = create_engine(
            url=settings.DATABASE_URL,
            echo=settings.DATABASE_LOGGING,
            connect_args={
                "check_same_thread": False,
            },  # for SQLite only
        )
        # create session factory
        self._session_maker = sessionmaker(
            # autocommit=False,
            # autoflush=False,
            bind=self.engine,
        )
        # generate model schemas
        with self.engine.begin() as conn:
            Base.metadata.drop_all(conn)
            Base.metadata.create_all(conn)

    @property
    def session_maker(self):
        return self._session_maker


_database: Optional[Database] = None


def get_db_session():
    global _database
    if not _database:
        _database = Database(settings=get_settings())
    with _database.session_maker() as session:
        yield session
