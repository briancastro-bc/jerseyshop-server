from sqlalchemy import Column, CHAR, ForeignKey, String

from app.core import Base
from app.common.helpers import generate_code

class SubCategory(Base):
    __tablename__ = 'subcategories'
    code = Column(CHAR(15), primary_key=True, nullable=False)
    name = Column(CHAR(50), unique=True, nullable=False)
    description = Column(String(300), nullable=True)
    #tags = Column() # TODO: convertir tags en un arreglo.
    category = Column(CHAR(15), ForeignKey('categories.code'), nullable=True) # FIXME: Nullable to False.
    
    def __init__(self, name: str, description: str=None, category: str=None) -> None:
        super().__init__()
        self.code = generate_code()
        self.name = name
        self.description = description
        self.category = category