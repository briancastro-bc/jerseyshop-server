from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import Product
from app.common.models import ProductModel

class ProductService:
    
    def __init__(self) -> None:
        pass
    
    async def get_all(self, db: AsyncSession):
        pass
    
    async def get_by_code(self, code: str, db: AsyncSession):
        pass
    
    async def create(self, product: ProductModel, db: AsyncSession):
        try:
            new_product = Product(
                name=product.name,
                sizes=product.sizes,
                stock=product.stock,
                photo=product.photos,
                price=product.price,
                color=product.colors,
                detail=product.detail,
                vat=product.vat,
                category=product.category,
                brand=product.brand,
                is_available=product.is_available
            )
            db.add(new_product)
            await db.commit()
            return new_product
        except Exception as e:
            raise HTTPException(
                400,
                {
                    "status": "fail",
                    "data": {
                        "message": "No pudimos crear el producto",
                        "exception": f"{e}"
                    }
                }
            )