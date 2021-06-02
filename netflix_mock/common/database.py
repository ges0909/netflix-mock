# async: https://docs.sqlalchemy.org/en/14/_modules/examples/asyncio/async_orm.html

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import sessionmaker

from netflix_mock.common.settings import Settings
from netflix_mock.common.singleton import Singleton

Base = declarative_base()


class Database(metaclass=Singleton):
    def __init__(self):
        settings = Settings()
        engine = create_engine(
            url=settings.database.url,
            echo=settings.database.logging,
            connect_args={
                "check_same_thread": False,  # for SQLite only
            },
        )
        # create session factory
        self._SessionLocal = sessionmaker(
            # autocommit=False,
            # autoflush=False,
            bind=engine,
        )
        # generate data model
        with engine.begin() as conn:
            if settings.database.drop_tables:
                Base.metadata.drop_all(conn)
            Base.metadata.create_all(conn)

    def session(self):
        with self._SessionLocal() as session:  # 'session_maker' is called
            yield session
        # session is closed by context manager
