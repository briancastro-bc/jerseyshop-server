import datetime
from sqlalchemy import Column, CHAR, String, TIMESTAMP
from sqlalchemy.orm import relationship

from app.core import Base
from app.common.helpers import generate_code

class Category(Base):
    __tablename__ = 'categories'
    code = Column(CHAR(10), primary_key=True, nullable=False)
    name = Column(CHAR(50), unique=True, nullable=False)
    description = Column(String(300), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow())
    sub_categories = relationship("SubCategory", back_populates="category")
    products = relationship("Product", back_populates="category")
    
    def __init__(
        self, 
        name: str, 
        description: str=None
    ) -> None:
        self.code = generate_code(length=10)
        self.name = name
        self.description = description