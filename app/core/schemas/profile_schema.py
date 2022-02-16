from sqlalchemy import Column, ForeignKey, String, CHAR
from sqlalchemy.orm import relationship

from app.database import Base

import uuid

class Profile(Base):
    __tablename__ = 'profiles'
    uid = Column(String(36), primary_key=True, nullable=False)
    user_uid = Column(String(36), ForeignKey('users.uid'), primary_key=True)
    user = relationship('User', back_populates='profile')
    phone_number = Column(CHAR(20), nullable=False)
    photo = Column(String(450), nullable=True)
    
    def __init__(
        self, 
        user_uid: str=None, 
        phone_number: str=None, 
        photo: str=None
    ) -> None:
        super().__init__()
        self.uid = str(uuid.uuid4())
        self.user_uid = user_uid
        self.phone_number = phone_number
        self.photo = photo