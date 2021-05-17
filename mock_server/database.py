from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import sessionmaker

# asnyc: https://docs.sqlalchemy.org/en/14/_modules/examples/asyncio/async_orm.html

Base = declarative_base()


class Database:
    def __init__(self, app_settings):
        self.engine = create_engine(
            url=app_settings.DATABASE_URL,
            echo=True,
            connect_args={"check_same_thread": False},  # for SQLite only
        )
        # create session factory
        self.SessionLocal = sessionmaker(
            # autocommit=False,
            # autoflush=False,
            bind=self.engine,
        )
        # generate models schema
        with self.engine.begin() as conn:
            Base.metadata.drop_all(conn)
            Base.metadata.create_all(conn)
