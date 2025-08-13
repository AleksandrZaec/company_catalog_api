from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.config.db import Base
from src.models.associations import organization_activity


class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey('activities.id', ondelete="CASCADE"), nullable=True, index=True)

    parent = relationship('Activity', remote_side=[id], back_populates='children')
    children = relationship(
        'Activity',
        back_populates='parent',
        remote_side=[parent_id],
        cascade='all, delete-orphan',
        lazy='selectin'
    )
    organizations = relationship(
        'Organization',
        secondary=organization_activity,
        back_populates='activities',
        lazy='selectin'
    )
