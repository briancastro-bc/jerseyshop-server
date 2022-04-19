from sqlalchemy import Column, CHAR, ForeignKey, String
from sqlalchemy.orm import relationship

from app.core import Base
from app.common.helpers import generate_code

class SubCategory(Base):
    __tablename__ = "subcategories"
    code = Column(CHAR(15), primary_key=True, nullable=False)
    name = Column(CHAR(50), unique=True, nullable=False)
    description = Column(String(300), nullable=True)
    category_id = Column(CHAR(10), ForeignKey("categories.code"), nullable=False)
    category = relationship("Category", back_populates="sub_categories")
    products = relationship("Product", back_populates="sub_category")
    
    def __init__(
        self, 
        name: str, 
        description: str|None,
        category_id: str
    ) -> None:
        self.code = generate_code()
        self.name = name
        self.description = description
        self.category_id = category_id