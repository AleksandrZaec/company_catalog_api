from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.config.db import Base
from src.models.associations import organization_activity


class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    building_id = Column(Integer, ForeignKey('buildings.id', ondelete="SET NULL"), nullable=True)

    building = relationship('Building', back_populates='organizations', lazy='joined')
    phones = relationship('Phone', back_populates='organization', cascade='all, delete', lazy='selectin')
    activities = relationship(
        'Activity',
        secondary=organization_activity,
        back_populates='organizations',
        lazy='selectin'
    )
