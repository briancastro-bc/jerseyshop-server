import datetime
from sqlalchemy import Column, CHAR, String, TIMESTAMP

from app.core import Base
from app.common.helpers import generate_code

class Color(Base):
    __tablename__ = 'colors'
    uid = Column(CHAR(10), primary_key=True, nullable=False)
    name = Column(String(30), unique=True, nullable=False)
    value = Column(CHAR(10), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow())
    
    def __init__(
        self,
        name: str,
        value: str
    ) -> None:
        self.uid = generate_code(length=10)
        self.name = name
        self.value = value