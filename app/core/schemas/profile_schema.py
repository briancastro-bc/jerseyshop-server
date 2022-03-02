from sqlalchemy import Column, ForeignKey, String, CHAR, Enum
from sqlalchemy.orm import relationship

from app.core.database import Base

import uuid, enum

class Gender(enum.Enum):
    male='m'
    female='f'
    other='o'

class Profile(Base):
    __tablename__ = 'profiles'
    uid = Column(String(36), primary_key=True, nullable=False)
    user_uid = Column(String(36), ForeignKey('users.uid'), primary_key=True)
    phone_number = Column(CHAR(20), nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    photo = Column(String(450), nullable=True)
    user = relationship('User', back_populates='profile')
    
    def __init__(
        self, 
        phone_number: str,
        gender: str,
        user_uid: str=None, 
        photo: str=None
    ) -> None:
        super().__init__()
        self.uid = str(uuid.uuid4())
        self.user_uid = user_uid
        self.phone_number = phone_number
        self.photo = photo
        self.gender = gender