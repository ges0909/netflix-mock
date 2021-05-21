from typing import Optional

from pydantic import BaseModel


class Success(BaseModel):
    detail: Optional[str] = "successful"
