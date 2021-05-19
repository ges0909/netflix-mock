from typing import List

import fastapi
from fastapi import Depends, HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from netflix_mock.auth import get_basic_auth
from netflix_mock.database import get_db_session
from netflix_mock.schemas.user import UserIn, UserOut
from netflix_mock.services import user_service

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
    session: Session = Depends(get_db_session),
) -> UserOut:
    """Updates the user data."""
    user_ = user_service.update_user_by_id(session=session, id=id, user=user)
    if user_:
        return UserOut(id=user_.id, username=user_.username)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"user id='{id}' not found",
    )


@router.get("/{id}", response_model=UserOut)
async def get_user_by_id(
    id: int,
    _: str = Depends(get_basic_auth),
    session: Session = Depends(get_db_session),
) -> UserOut:
    """Gets the user data."""
    user = user_service.get_user_by_id(session=session, id=id)
    if user:
        return UserOut(id=user.id, username=user.username)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"user id='{id}' not found",
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(
    id: int,
    _: str = Depends(get_basic_auth),
    session: Session = Depends(get_db_session),
) -> None:
    """Deletes the user."""
    if not user_service.delete_user_by_id(session, id=id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user id='{id}' not found",
        )


@router.get("/", response_model=List[UserOut])
async def get_all_users(
    _: str = Depends(get_basic_auth),
    session: Session = Depends(get_db_session),
) -> List[UserOut]:
    """Get all users."""
    return [UserOut(id=user.id, username=user.username) for user in user_service.get_all_users(session=session)]
