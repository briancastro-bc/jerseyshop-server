from fastapi import HTTPException
from sqlalchemy import delete, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import Category
from app.common.models import CategoryCreate, CategoryParcialUpdate

class CategoryService:
    
    @classmethod
    async def get_all(
        cls, 
        session: AsyncSession
    ):
        try:
            query = await session.execute(select(Category))
            db_categories = query.scalars().all()
            if db_categories:
                return db_categories
            return None
        except Exception:
            raise HTTPException(
                400,
                {
                    "status": "fail",
                    "data": {
                        "message": "No pudimos mostrar las categorias disponibles"
                    }
                }
            )
    
    async def get_by_code(self, code: str, db: AsyncSession):
        try:
            query = await db.execute(select(Category).where(Category.code == code))
            db_category = query.scalars().first()
            if db_category:
                return db_category
            return None
        except Exception:
            raise HTTPException(
                400,
                {
                    "status": "fail",
                    "data": {
                        "message": "No pudimos mostrar la categoria"
                    }
                }
            )
    
    async def create(self, category: CategoryCreate, db: AsyncSession):
        try:
            query = await db.execute(select(Category).where(Category.name == category.name))
            db_category = query.scalars().first()
            if not db_category:
                new_category = Category(
                    name=category.name,
                    description=category.description,
                )
                db.add(new_category)
                await db.commit()
                return new_category
            return None
        except Exception:
            raise HTTPException(
                400,
                {
                    "status": "fail",
                    "data": {
                        "message": "No pudimos crear la categoria",
                    }
                }
            )
    
    async def update(self):
        pass
    
    async def edit(self, code: str, category: CategoryParcialUpdate, db: AsyncSession):
        try:
            edit_category = await db.execute(
                update(Category)
                .where(Category.code == code)
                .values(**category.dict(exclude_unset=True)) # Toma los valores del modelo y los pasa como un diccionario
                # luego de ello, ignora los valores con null
            )
            await db.commit()
            return edit_category
        except Exception:
            return None
    
    async def delete(self, code: str, db: AsyncSession):
        try:
            await db.execute(delete(Category).where(Category.code == code))
            await db.commit()
            return True
        except Exception:
            return None