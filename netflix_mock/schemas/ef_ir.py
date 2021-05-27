from typing import List, Optional

from pydantic import BaseModel, Field


class ProvCustomerData(BaseModel):
    chargingType: Optional[str] = Field(default="cable", description="expected value 'cable'")
    externalIdentifier1: str
    """is on provisioning side (SBP) the serviceId"""
    products: List[str]


class ProfileCreation(BaseModel):
    pass


class Forbidden(BaseModel):
    message: str


class CustomerNotFound(BaseModel):
    message: str


class Error(BaseModel):
    message: str
