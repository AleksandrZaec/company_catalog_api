from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.config.db import Base


class Phone(Base):
    __tablename__ = "phones"

    id = Column(Integer, primary_key=True)
    number = Column(String, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"))

    organization = relationship("Organization", back_populates="phones")
