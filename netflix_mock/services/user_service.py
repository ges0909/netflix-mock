from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import now

import netflix_mock.models.user as models
import netflix_mock.schemas.user as schemas


def _get_user_by_id(session: Session, id_: int) -> models.User:
    return session.query(models.User).filter_by(id=id_).first()


def create_user(
    session: Session,
    user: schemas.UserCreate,
) -> models.User:
    user_ = models.User(
        username=user.username,
        password=user.password.get_secret_value(),
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    session.add(user_)
    session.commit()
    return user_


def update_user_by_id(
    session: Session,
    id_: int,
    user: schemas.UserUpdate,
) -> Optional[models.User]:
    if user_ := _get_user_by_id(session, id_):
        if "username" in user:
            user_.username = user.username
        if "password" in user:
            user_.password = user.password.get_secret_value() + "not_really_hashed"
        if "email" in user:
            user_.email = user.email
        if "last_name" in user:
            user_.last_name = user.last_name
        if "first_name" in user:
            user_.first_name = user.first_name
        user_.updated_at = now()
        session.add(user_)
        session.commit()
        return user_
    return None


def get_user_by_id(session: Session, id_: int) -> Optional[models.User]:
    if user_ := _get_user_by_id(session, id_):
        return user_
    return None


def delete_user_by_id(session: Session, id_: int) -> Optional[models.User]:
    if user_ := _get_user_by_id(session, id_):
        session.delete(user_)
        session.commit()
        return user_
    return None


def get_all_users(session: Session) -> List[models.User]:
    return session.query(models.User).all()
