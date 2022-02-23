from typing import Optional
from unicodedata import category

from pydantic import validator
from fastapi_utils.api_model import APIModel

from app.core.schemas import Sizes

import datetime

class ProductBase(APIModel):
    code: Optional[str]
    name: str
    photos: str
    price: float

class ProductCreate(ProductBase):
    stock: int
    colors: str
    vat: Optional[int]
    detail: Optional[str]
    sizes: Optional[Sizes]
    category: Optional[str]
    brand: Optional[str]
    is_available: Optional[bool] = True

class ProductModel(ProductCreate):
    created_at: Optional[datetime.datetime]

class ProductPartialUpdate(APIModel):
    name: Optional[str]
    photos: Optional[str]
    price: Optional[float]
    stock: Optional[int]
    colors: Optional[str]
    vat: Optional[int]
    detail: Optional[str]
    sizes: Optional[Sizes]
    category: Optional[str]
    brand: Optional[str]
    is_available: Optional[bool]