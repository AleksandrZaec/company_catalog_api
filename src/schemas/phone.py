from pydantic import BaseModel, ConfigDict


class PhoneBase(BaseModel):
    id: int
    number: str
    model_config = ConfigDict(from_attributes=True)
