from sqlalchemy import Column, CHAR, Float, ForeignKey, Integer, String, Enum, TIMESTAMP, Boolean

from app.core import Base
from app.common.helpers import generate_code

import enum, datetime

class Sizes(enum.Enum):
    extra_small='xs'
    small='s'
    medium='m'
    large='l'
    extra_large='xl'

class Product(Base):
    __tablename__ = 'products'
    code = Column(CHAR(25), primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    detail = Column(String(300), nullable=True)
    sizes = Column(Enum(Sizes), nullable=False)
    stock = Column(Integer, nullable=False)
    photos = Column(String(400), nullable=False) # TODO: converitr el campo a un arreglo.
    price = Column(Float, nullable=False)
    vat = Column(Integer, nullable=True)  #IVA equivalent
    colors = Column(CHAR(20), nullable=False) # TODO: convertir colors a un arreglo.
    category = Column(CHAR(15), ForeignKey('categories.code'), nullable=True) #FIXME: Nullable to False
    #subcategory = Column() #TODO: Agregar subcategorias a los productos.
    brand = Column(CHAR(15), ForeignKey('brands.code'), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.utcnow())
    is_available = Column(Boolean, nullable=False, default=True)
    
    def __init__(
        self,
        name: str,
        sizes: str,
        stock: int,
        photo: str,
        price: float,
        color: str,
        detail: str=None,
        vat: int=None,
        category: str=None,
        brand: str=None,
        is_available: bool=True
    ) -> None:
        super().__init__()
        self.code = generate_code(length=25)
        self.name = name
        self.detail = detail
        self.sizes = sizes
        self.stock = stock
        self.photos = photo
        self.price = price
        self.vat = vat
        self.colors = color
        self.category = category
        self.brand = brand
        self.is_available = is_available