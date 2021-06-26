from typing import Any, Dict, Optional

import yaml
from pydantic import BaseModel, Field, validate_arguments


@validate_arguments
def func(
    path: str,
    json_: Optional[Dict[str, Any]] = None,  # Field(alias="json", default=None),
    text: Optional[str] = None,
    xml: Optional[str] = None,
):
    return "Okay"


def test_1():
    assert func(path="/base", json_=dict(a=1, b=2, c=3)) == "Okay"


# --


class Body(BaseModel):
    json_: Optional[Dict[str, Any]] = Field(alias="json", default=None)
    text: Optional[str] = None
    xml: Optional[str] = None


@validate_arguments
def func2(
    path: str,
    body: Body,
):
    return "Okay"


def test_2():
    body = r"""
    json:
      a: 1
      b: 2
      c: 3
    """

    assert (
        func2(
            path="/base",
            body=yaml.load(body),
        )
        == "Okay"
    )


# '1. test step':
#   use: none
#   input:
#     body:
#       a: 1
#       b: 2
#       c: 3
#   output:
#     status: 201


# '1. test step':
#   use: none
#   input:
#     body:
#       json:
#         a: 1
#         b: 2
#         c: 3
#   output:
#     status: 201
