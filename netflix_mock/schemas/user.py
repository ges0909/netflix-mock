from pydantic import BaseModel, Field


class UserOut(BaseModel):
    id_: int = Field(alias="id")
    username: str


class UserIn(BaseModel):
    username: str
    password: str
