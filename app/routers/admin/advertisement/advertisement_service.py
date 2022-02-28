from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import Advertisement
from app.common.models import AdvertisementCreate

class AdvertisementService:
    
    def __init__(self) -> None:
        pass
    
    async def get_all(self, db: AsyncSession):
        try:
            query = await db.execute(select(Advertisement).order_by(Advertisement.time_ago))
            db_advertisements = query.scalars().all()
            if db_advertisements:
                return db_advertisements
            return None
        except:
            return None
    
    async def create(self, advertisement: AdvertisementCreate, db: AsyncSession):
        try:
            new_advertisement = Advertisement(
                title=advertisement.title,
                hyperlink=advertisement.hyperlink,
                description=advertisement.description
            )
            db.add(new_advertisement)
            await db.commit()
            return new_advertisement
        except Exception as e:
            raise HTTPException(400, {
                "status": "fail",
                "data": {
                    "message": "Ha ocurrido un error",
                    "exception": f"{e}"
                }
            })