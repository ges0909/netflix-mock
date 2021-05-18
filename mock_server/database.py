from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import sessionmaker

from mock_server.config import get_settings

# async: https://docs.sqlalchemy.org/en/14/_modules/examples/asyncio/async_orm.html

Base = declarative_base()

settings = get_settings()

engine = create_engine(
    url=settings.DATABASE_URL,
    echo=settings.DATABASE_LOGGING,
    connect_args={"check_same_thread": False},  # for SQLite only
)

# create session factory
Session = sessionmaker(
    # autocommit=False,
    # autoflush=False,
    bind=engine,
)

# generate model schemas
with engine.begin() as conn:
    Base.metadata.drop_all(conn)
    Base.metadata.create_all(conn)


def get_db_session():
    with Session() as session:
        yield session
