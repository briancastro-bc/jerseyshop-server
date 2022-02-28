from sqlalchemy import CHAR, Column, String, DateTime, Boolean, TIMESTAMP, Table, ForeignKey, Integer
from sqlalchemy.orm import relationship, backref

from app.core.database import Base, metadata

import datetime, uuid

user_groups = Table(
    'user_groups',
    metadata,
    Column('user_id', String(36), ForeignKey('users.uid'), primary_key=True),
    Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True)
)
    
user_permissions = Table(
    'user_permissions',
    metadata,
    Column('user_id', String(36), ForeignKey('users.uid'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)

user_favorites = Table(
    'user_favorites',
    metadata,
    Column('user_id', String(36), ForeignKey('users.uid'), primary_key=True),
    Column('product_code', CHAR(25), ForeignKey('products.code'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    uid = Column(String(36), primary_key=True, nullable=False)
    email = Column(String(70), unique=True, nullable=False)
    password = Column(String(450), nullable=True)
    name = Column(String(40), nullable=False)
    last_name = Column(String(60), nullable=False)
    birthday = Column(DateTime, nullable=False)
    is_verify = Column(Boolean, default=False)
    accept_advertising = Column(Boolean, default=False)
    accept_terms = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.datetime.utcnow())
    profile = relationship('Profile', back_populates='user', uselist=False)
    groups = relationship('Group', secondary=user_groups, lazy='joined', backref=backref('users_groups', lazy=True))
    permissions = relationship('Permission', secondary=user_permissions, lazy='joined', backref=backref('users_permissions', lazy=True))
    favorites = relationship('Product', secondary=user_favorites, lazy='joined', backref=backref('users_favorites', lazy=True))
    #room = relationship('Room')

    def __init__(
        self, 
        email: str=None, 
        name: str=None, 
        last_name: str=None, 
        birthday: str=None, 
        accept_advertising: bool=None, 
        accept_terms: bool=None, 
        password: str=None,
    ) -> None:
        super().__init__()
        self.uid = self.generate_uid()
        self.email = email
        self.password = password
        self.name = name
        self.last_name = last_name
        self.birthday = birthday
        self.accept_advertising = accept_advertising
        self.accept_terms = accept_terms

    @staticmethod
    def generate_uid() -> str:
        return str(uuid.uuid4())