from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.config.db import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=True)

    parent = relationship("Activity", remote_side=[id], backref="children", passive_deletes=True)
    organizations = relationship(
        "Organization",
        secondary="organization_activities",
        back_populates="activities"
    )
