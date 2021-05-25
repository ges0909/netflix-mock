from typing import Optional, List

from pydantic import BaseModel


class ProvCustomerData(BaseModel):
    chargingType: Optional[str] = "cable"
    externalIdentifier1: str
    products: List[str]


class ProfileCreation(BaseModel):
    pass


class Forbidden(BaseModel):
    message: str


class CustomerNotFound(BaseModel):
    message: str


class Error(BaseModel):
    message: str
