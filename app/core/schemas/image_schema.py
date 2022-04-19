from sqlalchemy import Column, CHAR, String, ForeignKey

from app.core import Base
from app.common.helpers import generate_code

class Image(Base):
    __tablename__ = 'images'
    uid = Column(CHAR(10), primary_key=True, nullable=False)
    product_id = Column(CHAR(25), ForeignKey("products.code"))
    url = Column(String(400), nullable=False)
    description = Column(String(300), nullable=True)
    
    def __init__(
        self,
        url: str,
        description: str,
        product_id: str=None
    ) -> None:
        self.uid = generate_code(length=10)
        self.product_id = product_id
        self.url = url
        self.description = description