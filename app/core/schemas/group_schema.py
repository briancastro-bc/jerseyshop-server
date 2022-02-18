from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.core.database import Base, metadata

groups_permissions = Table(
    'groups_permissions',
    metadata,
    Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    name = Column(String(60), nullable=False)
    code_name = Column(String(100), unique=True, nullable=False)
    permissions = relationship('Permission', secondary=groups_permissions, lazy='subquery', backref=backref('groups', lazy=True))