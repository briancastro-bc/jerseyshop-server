from sqlalchemy import Column, CHAR, String
from sqlalchemy.orm import relationship

from app.core import Base
from app.common.helpers import generate_code

class Brand(Base):
    __tablename__ = 'brands'
    code = Column(CHAR(15), primary_key=True, nullable=False)
    name = Column(CHAR(50), unique=True, nullable=False)
    logo = Column(String(400), nullable=False)
    product = relationship('Product')
    
    def __init__(self, name: str, logo: str) -> None:
        super().__init__()
        self.code = generate_code()
        self.name = name
        self.logo = logo