from pydantic import BaseModel, Field, SecretStr


class UserIn(BaseModel):
    username: str
    password: SecretStr

    class Config:
        schema_extra = {
            "example": {
                "username": "frankie",
                "password": "goes to hollywood",
            }
        }


class UserOut(BaseModel):
    id_: int = Field(alias="id")
    username: str
