from pydantic import BaseModel, ConfigDict


class PhoneBase(BaseModel):
    number: str


class PhoneCreate(PhoneBase):
    pass


class Phone(PhoneBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
