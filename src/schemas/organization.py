from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from src.schemas.phone import Phone
from src.schemas.activity import Activity
from src.schemas.building import Building


class OrganizationBase(BaseModel):
    name: str
    building_id: Optional[int] = None


class OrganizationCreate(OrganizationBase):
    phones: List[Phone] = []
    activity_ids: List[int] = []


class OrganizationUpdate(OrganizationBase):
    phones: Optional[List[Phone]] = None
    activity_ids: Optional[List[int]] = None


class OrganizationInDBBase(OrganizationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class Organization(OrganizationInDBBase):
    phones: List[Phone] = []
    activities: List[Activity] = []
    building: Optional[Building] = None
