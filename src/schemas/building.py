from pydantic import BaseModel, ConfigDict
from typing import Optional


class BuildingBase(BaseModel):
    address: str
    latitude: float
    longitude: float


class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BaseModel):
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class BuildingInDBBase(BuildingBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class Building(BuildingInDBBase):
    pass
