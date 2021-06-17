# async: https://docs.sqlalchemy.org/en/14/_modules/examples/asyncio/async_orm.html

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import sessionmaker

from netflix_mock.settings import get_settings

settings = get_settings()

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


def create_database_model():
    from netflix_mock.models.todo import Todo
    from netflix_mock.models.user import User

    # use models to avoid removal of local imports when code is refactored by IDE
    _ = User()
    _ = Todo()

    with engine.begin() as conn:
        Base.metadata.create_all(bind=conn)


def get_db_session():
    """create new database session, run sql stmt.s in yielded sessions and close session"""
    with SessionLocal() as session:
        yield session
