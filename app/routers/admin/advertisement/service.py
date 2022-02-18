from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas.advertisement_schema import Advertisement

from .model import AdvertisementCreate

class AdvertisementService:
    
    def __init__(self) -> None:
        pass
    
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