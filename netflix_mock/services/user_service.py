from typing import Optional, List

from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import now

from netflix_mock.models.user import User
from netflix_mock.schemas.user import UserIn


def _get_user_by_id(session: Session, id: int) -> User:
    return session.query(User).filter_by(id=id).first()


def create_user(session: Session, user: UserIn) -> User:
    password = user.password.get_secret_value() + "not_really_hashed"
    _user = User(username=user.username, hashed_password=password)
    session.add(_user)
    session.commit()
    return _user


def update_user_by_id(session: Session, id: int, user: UserIn) -> Optional[User]:
    _user = _get_user_by_id(session=session, id=id)
    if _user:
        _user.username = user.username
        _user.password = user.password.get_secret_value() + "not_really_hashed"
        _user.updated_at = now()
        session.add(_user)
        session.commit()
        return _user
    return None


def get_user_by_id(session: Session, id: int) -> Optional[User]:
    _user = _get_user_by_id(session=session, id=id)
    if _user:
        return _user
    return None


def delete_user_by_id(session: Session, id: int) -> Optional[User]:
    _user = _get_user_by_id(session=session, id=id)
    if _user:
        session.delete(_user)
        session.commit()
        return _user
    return None


def get_all_users(session: Session) -> List[User]:
    return session.query(User).all()
