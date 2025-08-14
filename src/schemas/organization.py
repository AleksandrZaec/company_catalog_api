from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from src.schemas.activity import ActivityBase, ActivityRead
from src.schemas.building import BuildingBase
from src.schemas.phone import PhoneBase


class OrganizationBase(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class OrganizationRead(OrganizationBase):
    building: Optional[BuildingBase] = None
    activities: List[ActivityBase] = Field(default_factory=list)
    phones: List[PhoneBase] = Field(default_factory=list)


ActivityRead.model_rebuild()
