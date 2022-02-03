from sqlalchemy import TIMESTAMP, Column, Boolean, CHAR, ForeignKey, Integer, Table, String
from sqlalchemy.orm import relationship, backref

from app.database import Base, metadata

import datetime

rooms_users_table = Table(
    'rooms_users',
    metadata,
    Column('user_id', String(36), ForeignKey('users.uid'), primary_key=True),
    Column('room_code', CHAR(10), ForeignKey('rooms.code'), primary_key=True)
)

class Room(Base):
    __tablename__ = 'rooms'
    code = Column(CHAR(10), primary_key=True, nullable=False)
    name = Column(CHAR(30), unique=True, nullable=False)
    limit = Column(Integer, nullable=False, default=2)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.utcnow())
    users = relationship('User', secondary=rooms_users_table, lazy='subquery', backref=backref('rooms', lazy=True))  