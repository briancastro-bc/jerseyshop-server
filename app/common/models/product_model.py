import datetime
from pydantic import Field, validator
from fastapi_utils.api_model import APIModel

from .image_model import ImageModel
from .size_model import SizeModel
from .color_model import ColorModel

class ProductBase(APIModel):
    code: str | None = Field(None)
    name: str = Field(..., max_length=100)
    price: float = Field(...)

class ProductCreate(ProductBase):
    description: str = Field(..., max_length=400)
    stock: int = Field(...)
    images: list[ImageModel] = Field(...)
    sizes: list[SizeModel] = Field(...)
    colors: list[ColorModel] = Field(...)
    vat: int | None = Field(None)
    category_id: str = Field(..., max_length=10)
    sub_category_id: str = Field(..., max_length=10)
    brand_id: str = Field(..., max_length=15)

class ProductModel(ProductCreate):
    is_available: bool | None = Field(None)
    created_at: datetime.datetime | None = Field(None)

class ProductPartialUpdate(APIModel):
    # TODO://modify fields.
    name: str | None
    photos: str | None
    price: float | None
    stock: int | None
    colors: str | None
    vat: int | None
    description: str | None
    sizes: list[str] | None
    category: str | None
    brand: str | None
    is_available: bool | None