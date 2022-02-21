from typing import Optional

from pydantic import validator
from fastapi_utils.api_model import APIModel

class CategoryBase(APIModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryModel(CategoryCreate):
    code: str

class CategoryParcialUpdate(APIModel):
    name: Optional[str]
    description: Optional[str]
    code: Optional[str]