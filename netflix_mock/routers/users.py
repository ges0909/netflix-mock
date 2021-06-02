from typing import List

import fastapi
from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from netflix_mock.common.database import Database
from netflix_mock.depends.basic_auth import mock_user
from netflix_mock.schemas.error import Error
from netflix_mock.schemas.user import UserCreate, UserIn, UserOut
from netflix_mock.services import user_service

router = fastapi.APIRouter()


@router.post(
    path="",
    description="Create an user",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOut,
    # response_model_exclude={"password"},
    responses={
        401: {"model": Error},
        500: {"model": Error},
    },
)
async def create_user(
    user: UserCreate,
    _: None = Depends(mock_user),
    session: Session = Depends(Database().session),
) -> UserOut:
    """
    Create an user:

    - **username**: each user must have a name
    - **password**: each user must have a password
    """
    if user_ := user_service.create_user(session, user):
        return UserOut.from_orm(user_)


@router.put(
    path="/{id}",
    description="Update an user",
    response_model=UserOut,
    # response_model_exclude={"password"},
    responses={
        401: {"model": Error},
        404: {"model": Error},
        500: {"model": Error},
    },
)
async def update_user(
    user: UserIn,
    id_: int = Path(..., alias="id"),
    _: None = Depends(mock_user),
    session: Session = Depends(Database().session),
) -> UserOut:
    """Updates the user data."""
    if user_ := user_service.update_user_by_id(session, id_, user):
        return UserOut.from_orm(user_)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"user id='{id}' not found",
    )


@router.get(
    path="/{id}",
    description="Get an user by id",
    response_model=UserOut,
    responses={
        401: {"model": Error},
        404: {"model": Error},
        500: {"model": Error},
    },
)
async def get_user_by_id(
    id_: int = Path(..., alias="id"),
    _: None = Depends(mock_user),
    session: Session = Depends(Database().session),
) -> UserOut:
    """Gets the user data."""
    if user_ := user_service.get_user_by_id(session, id_):
        return UserOut.from_orm(user_)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"user id='{id_}' not found",
    )


@router.delete(
    path="/{id}",
    description="Delete an user by id",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"model": Error},
        404: {"model": Error},
        500: {"model": Error},
    },
)
async def delete_user_by_id(
    id_: int = Path(..., alias="id"),
    _: None = Depends(mock_user),
    session: Session = Depends(Database().session),
) -> None:
    """Deletes the user."""
    if not user_service.delete_user_by_id(session, id_):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user id='{id_}' not found",
        )


@router.get(
    path="/",
    description="Get all users",
    response_model=List[UserOut],
    responses={
        401: {"model": Error},
        500: {"model": Error},
    },
)
async def get_all_users(
    _: None = Depends(mock_user),
    session: Session = Depends(Database().session),
) -> List[UserOut]:
    """Get all users."""
    return [UserOut.from_orm(user_) for user_ in user_service.get_all_users(session=session)]
