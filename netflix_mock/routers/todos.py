import fastapi
from fastapi import Depends, status
from sqlalchemy.orm import Session

import netflix_mock.models.todo as models
import netflix_mock.schemas.todo as schemas
from netflix_mock.database import Database
from netflix_mock.depends.basic_auth import api_user
from netflix_mock.schemas.error import Error

router = fastapi.APIRouter()


@router.post(
    path="",
    description="Add a todo task",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Todo,
    responses={
        401: {"model": Error},
        500: {"model": Error},
    },
)
async def add_todo(
    user: schemas.TodoCreate,
    _: None = Depends(api_user),
    session: Session = Depends(Database().session),
) -> schemas.Todo:
    # user_: models.User = user_service.create_user(session, user)
    # return schemas.User.from_orm(user_)
    user_: models.Todo = None
    return schemas.Todo(id=1, text="Any task", completed=True)
