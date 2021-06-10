import fastapi
from fastapi import Depends, status
from sqlalchemy.orm import Session

import netflix_mock.schemas.todo as schemas
from netflix_mock.database import get_session
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
    dependencies=[Depends(api_user)],
)
async def add_todo(
    user: schemas.TodoCreate,
    session: Session = Depends(get_session),
) -> schemas.Todo:
    return schemas.Todo(id=1, text="Any task", completed=True)
