from pydantic import BaseModel, ConfigDict


class BuildingBase(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float
    model_config = ConfigDict(from_attributes=True)

