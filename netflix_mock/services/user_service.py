import hashlib
import os
from typing import List, Optional, Tuple

from pydantic import SecretStr
from sqlalchemy.orm import Session

import netflix_mock.models.user as models
import netflix_mock.schemas.user as schemas


def _get_user_by_id(session: Session, id_: int) -> models.User:
    return session.query(models.User).filter_by(id=id_).first()


def _create_hash_key(password: SecretStr) -> Tuple[bytes, bytes]:
    salt = os.urandom(32)  # store together with password
    key = hashlib.pbkdf2_hmac(
        "sha256",  # hash digest algorithm for HMAC
        password.get_secret_value().encode("utf-8"),  # 'encode' to convert password to bytes
        salt,
        100000,  # it is recommended to use at least 100,000 iterations of SHA-256
        dklen=128,  # get a 128 byte key
    )
    return key, salt


def create_user(
    session: Session,
    user: schemas.UserCreate,
) -> models.User:
    hash_key, salt = _create_hash_key(password=user.password)
    user_ = models.User(
        username=user.username,
        password_hash_key=hash_key,
        salt=salt,
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
        if user.username:
            user_.username = user.username
        if user.password:
            user_.password_hash_key, user_.salt = _create_hash_key(password=user.password)
        if user.email:
            user_.email = user.email
        if user.first_name:
            user_.first_name = user.first_name
        if user.last_name:
            user_.last_name = user.last_name
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
