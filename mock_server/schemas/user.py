from pydantic import BaseModel


class UserOut(BaseModel):
    id: int
    username: str


class UserIn(BaseModel):
    username: str
    password: str
