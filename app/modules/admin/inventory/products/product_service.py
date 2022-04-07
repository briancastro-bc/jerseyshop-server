from fastapi import HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import Product
from app.common.models import ProductModel, ProductPartialUpdate

class ProductService:
    
    def __init__(self) -> None:
        pass
    
    async def get_all(self, db: AsyncSession):
        try:
            query = await db.execute(select(Product))
            db_products = query.scalars().fetchall()
            if db_products:
                return db_products
            return None
        except Exception:
            return None
    
    async def get_by_code(self, code: str, db: AsyncSession):
        try:
            query = await db.execute(select(Product).where(Product.code == code))
            db_product = query.scalars().first()
            if db_product:
                return db_product
            return None
        except Exception:
            return None
    
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
    
    async def update(self):
        pass
    
    async def edit(self, product: ProductPartialUpdate, code: str, db: AsyncSession):
        try:
            edit_product = await db.execute(
                update(Product)
                .values(**product.dict(exclude_unset=True))
                .where(Product.code == code)
            )
            await db.commit()
            return edit_product
        except Exception:
            return None
    
    async def delete(self, code: str, db: AsyncSession):
        try:
            await db.execute(
                delete(Product)
                .where(Product.code == code)
            )
            await db.commit()
            return True
        except Exception:
            return None