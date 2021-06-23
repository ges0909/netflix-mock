from typing import List

import fastapi
from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

import netflix_mock.models.user as models
import netflix_mock.schemas.user as schemas
from netflix_mock.database import get_db_session
from netflix_mock.schemas.api_error import ApiError
from netflix_mock.services import user_service

router = fastapi.APIRouter()


@router.post(
    path="",
    description="Add new user",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.User,
    response_model_exclude={"password"},
    responses={
        401: {"model": ApiError},
        500: {"model": ApiError},
    },
)
async def create_user(
    user: schemas.UserCreate,
    session: Session = Depends(get_db_session),
) -> schemas.User:
    """
    Create an user:

    - **username**: each user must have a name
    - **password**: each user must have a password
    """
    user_: models.User = user_service.create_user(session, user)
    return schemas.User.from_orm(user_)


@router.put(
    path="/{id}",
    description="Update existing user",
    response_model=schemas.User,
    response_model_exclude={"password"},
    responses={
        401: {"model": ApiError},
        404: {"model": ApiError},
        500: {"model": ApiError},
    },
)
async def update_user(
    user: schemas.UserUpdate,
    id_: int = Path(..., alias="id"),
    session: Session = Depends(get_db_session),
) -> schemas.User:
    """Updates the user data."""
    user_: models.User = user_service.update_user_by_id(session, id_, user)
    if user_:
        return schemas.User.from_orm(user_)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"user id='{id}' not found",
    )


@router.get(
    path="/{id}",
    description="Get user by id",
    response_model=schemas.User,
    response_model_exclude={"password"},
    responses={
        401: {"model": ApiError},
        404: {"model": ApiError},
        500: {"model": ApiError},
    },
)
async def get_user_by_id(
    id_: int = Path(..., alias="id"),
    session: Session = Depends(get_db_session),
) -> schemas.User:
    """Gets the user data."""
    if user_ := user_service.get_user_by_id(session, id_):
        return schemas.User.from_orm(user_)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"user id='{id_}' not found",
    )


@router.delete(
    path="/{id}",
    description="Delete user by id",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"model": ApiError},
        404: {"model": ApiError},
        500: {"model": ApiError},
    },
)
async def delete_user_by_id(
    id_: int = Path(..., alias="id"),
    session: Session = Depends(get_db_session),
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
    response_model=List[schemas.User],
    response_model_exclude={"password"},
    responses={
        401: {"model": ApiError},
        500: {"model": ApiError},
    },
)
async def get_all_users(
    session: Session = Depends(get_db_session),
) -> List[schemas.User]:
    """Get all users."""
    return [schemas.User.from_orm(user_) for user_ in user_service.get_all_users(session=session)]
