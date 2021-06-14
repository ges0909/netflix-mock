import fastapi
from fastapi import Depends, status
from sqlalchemy.orm import Session

import netflix_mock.schemas.todo as schemas
from netflix_mock.database import get_db_session
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
    session: Session = Depends(get_db_session),
) -> schemas.Todo:
    r"""This is an example of a module level function.

    Function parameters should be documented in the ``Args`` section. The name
    of each parameter is required. The type and description of each parameter
    is optional, but should be included if not obvious.

    If \*args or \*\*kwargs are accepted,
    they should be listed as ``*args`` and ``**kwargs``.

    The format for a parameter is:

        name (type): description
            The description may span multiple lines. Following
            lines should be indented. The "(type)" is optional.

            Multiple paragraphs are supported in parameter
            descriptions.

    ## Alias:
    add todo

    Args:
        param1 (int): The first parameter.
        param2 (:obj:`str`, optional): The second parameter. Defaults to None.
            Second line of description should be indented.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        bool: True if successful, False otherwise.

        The return type is optional and may be specified at the beginning of
        the ``Returns`` section followed by a colon.

        The ``Returns`` section may span multiple lines and paragraphs.
        Following lines should be indented to match the first line.

        The ``Returns`` section supports any reStructuredText formatting,
        including literal blocks::

            {
                'param1': param1,
                'param2': param2
            }

    Raises:
        AttributeError: The ``Raises`` section is a list of all exceptions
            that are relevant to the interface.
        ValueError: If `param2` is equal to `param1`.

    Examples:
        Examples should be written in doctest format, and should illustrate how
        to use the function.

        >>> print([i for i in example_generator(4)])
        [0, 1, 2, 3]

    """
    return schemas.Todo(id=1, text="Any task", completed=True)
