from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class ActivityBase(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


class ActivityRead(ActivityBase):
    children: List["ActivityRead"] = Field(default_factory=list)
