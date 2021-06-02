from typing import Optional

from pydantic import BaseModel, EmailStr, Field, SecretStr


class UserCreate(BaseModel):
    username: str
    password: SecretStr
    email: EmailStr
    first_name: str
    last_name: str

    class Config:
        schema_extra = {
            "example": {
                "username": "frankie",
                "password": "goes to hollywood",
                "email": "frankie@hollywood.de",
                "first_name": "Holly",
                "last_name": "Johnson",
            }
        }


class _User(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]


class UserIn(_User):
    password: Optional[SecretStr]

    class Config:
        schema_extra = {
            "example": {
                "username": "frankie",
                "password": "goes to hollywood",
                "email": "frankie@hollywood.de",
                "first_name": "Holly",
                "last_name": "Johnson",
            }
        }


class UserOut(_User):
    id_: int = Field(alias="id", ge=0)

    class Config:
        orm_mode = True
