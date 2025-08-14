from sqlalchemy import Table, Column, Integer, ForeignKey
from src.config.db import Base

organization_activity = Table(
    'organization_activity',
    Base.metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id', ondelete="CASCADE"), primary_key=True),
    Column('activity_id', Integer, ForeignKey('activities.id', ondelete="CASCADE"), primary_key=True),
    extend_existing=True
)
