import uuid
from sqlalchemy import Column, String, Date, DateTime, Boolean, TIMESTAMP, Table, ForeignKey, Integer
from sqlalchemy.orm import relationship, backref
from fastapi_utils.guid_type import GUID

from app.database import Base, metadata

import datetime, uuid

user_groups = Table('user_groups',
    metadata,
    Column('user_id', String(36), ForeignKey('users.uid'), primary_key=True),
    Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True)
)
    
user_permissions = Table('user_permissions',
    metadata,
    Column('user_id', String(36), ForeignKey('users.uid'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    uid = Column(String(36), primary_key=True, nullable=False, default=str(uuid.uuid4()))
    email = Column(String(70), unique=True, nullable=False)
    password = Column(String(450), nullable=True)
    name = Column(String(40), nullable=False)
    last_name = Column(String(60), nullable=False)
    birthday = Column(DateTime, nullable=False)
    is_verify = Column(Boolean, default=False)
    accept_advertising = Column(Boolean, default=False)
    accept_terms = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.datetime.utcnow())
    groups = relationship('Group', secondary=user_groups, lazy='subquery', backref=backref('users', lazy=True))
    permissions = relationship('Permission', secondary=user_permissions, lazy='subquery', backref=backref('users', lazy=True))