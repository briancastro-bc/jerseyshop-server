from sqlalchemy import Column, CHAR, String
from sqlalchemy.orm import relationship

from app.core import Base
from app.common.helpers import generate_code

class Category(Base):
    __tablename__ = 'categories'
    code = Column(CHAR(15), primary_key=True, nullable=False)
    name = Column(CHAR(50), unique=True, nullable=False)
    description = Column(String(300), nullable=True)
    product = relationship('Product', backref='product_category')
    subcategory = relationship('SubCategory', backref='subcategory_category')
    
    def __init__(
        self, 
        name: str, 
        description: str=None
    ) -> None:
        super().__init__()
        self.code = generate_code()
        self.name = name
        self.description = description