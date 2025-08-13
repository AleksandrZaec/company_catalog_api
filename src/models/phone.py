from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.config.db import Base


class Phone(Base):
    __tablename__ = 'phones'

    id = Column(Integer, primary_key=True)
    number = Column(String(50), nullable=False, index=True)
    organization_id = Column(Integer, ForeignKey('organizations.id', ondelete="CASCADE"), nullable=False, index=True)

    organization = relationship('Organization', back_populates='phones')
