from sqlalchemy.orm import Session

from mock_server.models.user import User
from mock_server.schemas.user import UserIn


def create_user(sess: Session, user: UserIn) -> User:
    password = user.password + "notreallyhashed"
    user_ = User(username=user.username, hashed_password=password)
    sess.add(user_)
    sess.commit()
    return user_


def update_user(sess: Session, id: int, user: UserIn) -> User:
    user_ = sess.query(User).filter_by(id=id).first()
    user_.username = user.username
    user_.password = user.password + "notreallyhashed"
    sess.add(user_)
    sess.commit()
    return user_


def read_user_by_id(sess: Session, id: int) -> User:
    return sess.query(User).filter_by(id=id).first()


def delete_user_by_id(sess: Session, id: int) -> User:
    user_ = sess.query(User).filter_by(id=id).first()
    sess.delete(user_)
    sess.commit()
    return user_
