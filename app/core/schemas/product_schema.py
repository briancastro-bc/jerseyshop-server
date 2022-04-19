import datetime
from sqlalchemy import (
    Boolean, 
    Column, 
    CHAR, 
    Float, 
    ForeignKey, 
    Integer, 
    String, 
    TIMESTAMP, 
    Table
)
from sqlalchemy.orm import relationship

from app.core import Base, metadata
from app.common.helpers import generate_code

product_sizes = Table(
    "product_sizes",
    metadata,
    Column("product_id", ForeignKey("products.code")),
    Column("size_id", ForeignKey("sizes.uid"))
)

product_colors = Table(
    "product_colors",
    metadata,
    Column("product_id", ForeignKey("products.code")),
    Column("color_id", ForeignKey("colors.uid"))
)

class Product(Base):
    __tablename__ = "products"
    code = Column(CHAR(25), primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(400), nullable=False)
    stock = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    vat = Column(Integer, nullable=True)
    category_id = Column(CHAR(10), ForeignKey("categories.code"), nullable=False)
    sub_category_id = Column(CHAR(10), ForeignKey("subcategories.code"), nullable=False)
    brand_id = Column(CHAR(15), ForeignKey("brands.code"), nullable=True)
    is_available = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow())
    category = relationship("Category", back_populates="products")
    sub_category = relationship("SubCategory", back_populates="products")
    sizes = relationship("Size", secondary=product_sizes)
    colors = relationship("Color", secondary=product_colors)
    images = relationship("Image")
    
    def __init__(
        self,
        name: str,
        description: str,
        stock: int,
        price: float,
        category: str,
        sub_category: str,
        vat: int|None,
        brand: str|None,
        is_available: bool=True
    ) -> None:
        self.code = generate_code(length=25)
        self.name = name
        self.description = description
        self.stock = stock
        self.price = price
        self.vat = vat
        self.category_id = category
        self.sub_category_id = sub_category
        self.brand_id = brand
        self.is_available = is_available