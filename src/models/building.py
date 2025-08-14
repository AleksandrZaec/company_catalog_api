from sqlalchemy import Column, Integer, String, Float, Index
from sqlalchemy.orm import relationship
from src.config.db import Base


class Building(Base):
    __tablename__ = 'buildings'

    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    organizations = relationship('Organization', back_populates='building', cascade='all, delete')

    __table_args__ = (
        Index('ix_building_coords', 'latitude', 'longitude'),
    )
