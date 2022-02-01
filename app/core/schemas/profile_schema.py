from sqlalchemy import Column, ForeignKey, String, CHAR
from sqlalchemy.orm import relationship, backref

from app.database import Base

import uuid

class Profile(Base):
    __tablename__ = 'profiles'
    uid = Column(String(36), primary_key=True, nullable=False, default=str(uuid.uuid4()))
    user_uid = Column(String(36), ForeignKey('users.uid'))
    user = relationship('User', backref=backref('profiles', uselist=False))
    phone_number = Column(CHAR(20), nullable=False)
    photo = Column(String(450), nullable=True)