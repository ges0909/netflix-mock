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
                "password": "relax",
                "email": "frankie.goes.to@hollywood",
                "first_name": "Holly",
                "last_name": "Johnson",
            },
        }


class UserUpdate(BaseModel):
    username: Optional[str]
    password: Optional[SecretStr]
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]

    class Config:
        exclude_none = True
        schema_extra = {
            "example": {
                "username": "frankie",
                "password": "relax",
                "email": "frankie.goes.to@hollywood",
                "first_name": "Holly",
                "last_name": "Johnson",
            },
        }


class User(UserUpdate):
    id_: int = Field(alias="id", ge=0)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "frankie",
                "email": "frankie.goes.to@hollywood",
                "first_name": "Holly",
                "last_name": "Johnson",
                "id": 1,
            }
        }
