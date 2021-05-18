from typing import Optional

from sqlalchemy.orm import Session

from mock_server.models.user import User
from mock_server.schemas.user import UserIn


def _read_user_by_id(sess: Session, id: int) -> User:
    return sess.query(User).filter_by(id=id).first()


def create_user(sess: Session, user: UserIn) -> User:
    password = user.password + "not_really_hashed"
    _user = User(username=user.username, hashed_password=password)
    sess.add(_user)
    sess.commit()
    return _user


def update_user(sess: Session, id: int, user: UserIn) -> Optional[User]:
    if _user := _read_user_by_id(sess=sess, id=id):
        _user.username = user.username
        _user.password = user.password + "not_really_hashed"
        sess.add(_user)
        sess.commit()
        return _user
    return None


def read_user_by_id(sess: Session, id: int) -> Optional[User]:
    if _user := _read_user_by_id(sess=sess, id=id):
        return _user
    return None


def delete_user_by_id(sess: Session, id: int) -> Optional[User]:
    if _user := _read_user_by_id(sess=sess, id=id):
        sess.delete(_user)
        sess.commit()
        return _user
    return None
