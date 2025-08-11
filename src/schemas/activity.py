from pydantic import BaseModel
from typing import Optional, List
from pydantic import Field, ConfigDict


class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[int] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None


class ActivityInDBBase(ActivityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class Activity(ActivityInDBBase):
    children: List["Activity"] = Field(default_factory=list)


Activity.update_forward_refs()
