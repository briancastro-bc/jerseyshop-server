import datetime
from sqlalchemy import Column, CHAR, String, TIMESTAMP

from app.core import Base
from app.common.helpers import generate_code

class Size(Base):
    __tablename__ = 'sizes'
    uid = Column(CHAR(10), primary_key=True, nullable=False)
    value = Column(String(50), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow())
    
    def __init__(
        self,
        value: str
    ) -> None:
        self.uid = generate_code(length=10)
        self.value = value