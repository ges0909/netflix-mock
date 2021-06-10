# async: https://docs.sqlalchemy.org/en/14/_modules/examples/asyncio/async_orm.html

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import sessionmaker

from netflix_mock.settings import Settings
from netflix_mock.singleton import Singleton

Base = declarative_base()


class Database(metaclass=Singleton):
    def __init__(self):
        settings = Settings()
        self._engine = create_engine(
            url=settings.database.url,
            echo=settings.database.logging,
            connect_args={
                "check_same_thread": False,  # for SQLite only
            },
        )
        # create session factory
        self._Session = sessionmaker(
            # autocommit=False,
            # autoflush=False,
            bind=self._engine,
        )

    def session(self):
        with self._Session() as session:  # 'session_maker' is called
            yield session
        # session is closed by context manager

    def create(self):
        """generate data model"""
        # import netflix_mock.models.user
        # import netflix_mock.models.todo

        settings = Settings()
        with self._engine.begin() as conn:
            if settings.database.drop_tables:
                Base.metadata.drop_all(conn)
            Base.metadata.create_all(bind=conn)
