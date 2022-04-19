from fastapi import HTTPException
from sqlalchemy import select, update, delete, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import Product
from app.common.models import ProductModel, ProductPartialUpdate

class ProductService:
    
    @classmethod
    async def get_all(
        cls,
        *,
        order_by: int,
        limit: int,
        skip: int,
        session: AsyncSession
    ) -> list[Product]:
        try:
            result = await session.execute(
                text("SELECT * FROM products ORDER BY :order_by ASC LIMIT :limit OFFSET :skip").\
                    bindparams(
                        order_by=order_by,
                        limit=limit,
                        skip=skip
                    )
            )
            products: list[Product] = result.all()
        except Exception:
            raise HTTPException(
                400,
                "No se pudieron mostrar los productos"
            )
        else:
            return products
    
    @classmethod
    async def get(
        cls, 
        code: str, 
        session: AsyncSession
    ) -> Product:
        try:
            result = await session.execute(
                select(Product).where(Product.code == code)
            )
            product: Product = result.scalars().first()
        except Exception:
            raise HTTPException(
                400,
                "No se pudo mostrar el producto"
            )
        else:
            return product
    
    @classmethod
    async def create(
        cls, 
        product: ProductModel, 
        session: AsyncSession
    ) -> Product:
        try:
            """new_product = Product(
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
            )"""
            new_product = Product(
                **product.dict(
                    exclude_unset=True
                )
            )
            session.add(new_product)
            await session.commit()
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
        else:
            return new_product
    
    @classmethod
    async def update(cls):
        pass
    
    @classmethod
    async def edit(
        cls, 
        code: str,
        product: ProductPartialUpdate,
        session: AsyncSession
    ):
        try:
            edited_product = await session.execute(
                update(Product)
                .values(**product.dict(exclude_unset=True))
                .where(Product.code == code)
            )
            await session.commit()
        except Exception:
            raise HTTPException(
                400,
                "No se pudo editar el producto"
            )
        else:
            return edited_product
    
    @classmethod
    async def delete(
        cls, 
        code: str, 
        session: AsyncSession
    ) -> bool | None:
        try:
            await session.execute(
                delete(Product).where(Product.code == code)
            )
            await session.commit()
        except Exception:
            raise HTTPException(
                400,
                "No se pudo eliminar el producto"
            )
        else:
            return True