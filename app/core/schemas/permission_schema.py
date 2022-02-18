from sqlalchemy import Column, Integer, String

from app.core.database import Base

class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    name = Column(String(60), nullable=False)
    code_name = Column(String(100), unique=True, nullable=False)