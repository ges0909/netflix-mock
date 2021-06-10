# async: https://docs.sqlalchemy.org/en/14/_modules/examples/asyncio/async_orm.html

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import sessionmaker

from netflix_mock.settings import Settings

settings = Settings()

Base = declarative_base()


engine = create_engine(
    url=settings.database.url,
    echo=settings.database.logging,
    connect_args={"check_same_thread": False},  # for SQLite only
)

SessionLocal = sessionmaker(  # 'SessionLocal' is a class
    # autocommit=False,
    # autoflush=False,
    bind=engine,
)


def create_model():
    with engine.begin() as conn:
        # import netflix_mock.models.user
        # import netflix_mock.models.todo

        if settings.database.drop_tables:
            Base.metadata.drop_all(conn)
        Base.metadata.create_all(bind=conn)


def get_session():
    """create new database session, run sql stmt.s in yielded sessions and close session"""
    with SessionLocal() as session:
        yield session
