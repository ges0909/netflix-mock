import fastapi
from fastapi import Depends, HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from mock_server.auth import get_basic_auth
from mock_server.db import get_db_session
from mock_server.schemas.user import UserIn, UserOut
from mock_server.services import user_service

router = fastapi.APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(
    user: UserIn,
    _: str = Depends(get_basic_auth),
    session: Session = Depends(get_db_session),
) -> UserOut:
    """Creates a new user."""
    user_ = user_service.create_user(session=session, user=user)
    return UserOut(id=user_.id, username=user_.username)


@router.put("/{id}", response_model=UserOut)
async def update_user(
    id: int,
    user: UserIn,
    _: str = Depends(get_basic_auth),
    sess: Session = Depends(get_db_session),
) -> UserOut:
    """Updates the user data."""
    if user_ := user_service.update_user_by_id(session=sess, id=id, user=user):
        return UserOut(id=user_.id, username=user_.username)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"user id='{id}' not found",
    )


@router.get("/{id}", response_model=UserOut)
async def read_user_by_id(
    id: int,
    _: str = Depends(get_basic_auth),
    sess: Session = Depends(get_db_session),
) -> UserOut:
    """Gets the user data."""
    if user := user_service._read_user_by_id(sess=sess, id=id):
        return UserOut(id=user.id, username=user.username)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"user id='{id}' not found",
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(
    id: int,
    _: str = Depends(get_basic_auth),
    sess: Session = Depends(get_db_session),
) -> None:
    """Deletes the user."""
    if not user_service.delete_user_by_id(sess, id=id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user id='{id}' not found",
        )
