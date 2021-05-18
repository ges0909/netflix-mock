from typing import Optional, List

from sqlalchemy.orm import Session

from mock_server.models.user import User
from mock_server.schemas.user import UserIn


def _get_user_by_id(session: Session, id: int) -> User:
    return session.query(User).filter_by(id=id).first()


def create_user(session: Session, user: UserIn) -> User:
    password = user.password + "not_really_hashed"
    _user = User(username=user.username, hashed_password=password)
    session.add(_user)
    session.commit()
    return _user


def update_user_by_id(session: Session, id: int, user: UserIn) -> Optional[User]:
    if _user := _get_user_by_id(session=session, id=id):
        _user.username = user.username
        _user.password = user.password + "not_really_hashed"
        session.add(_user)
        session.commit()
        return _user
    return None


def get_user_by_id(session: Session, id: int) -> Optional[User]:
    if _user := _get_user_by_id(session=session, id=id):
        return _user
    return None


def delete_user_by_id(session: Session, id: int) -> Optional[User]:
    if _user := _get_user_by_id(session=session, id=id):
        session.delete(_user)
        session.commit()
        return _user
    return None


def get_all_users(session: Session) -> List[User]:
    return session.query(User).all()
