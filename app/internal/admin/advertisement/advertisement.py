from typing import List
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

from app.core.http import HttpResponseBadRequest, HttpResponseCreated
from app.core.schemas import Advertisement
from app.database import get_session

from .model import AdvertisementCreate, AdvertisementModel
from .service import AdvertisementService

router = InferringRouter()

@cbv(router)
class AdvertisementController:
    
    def __init__(self) -> None:
        self.advertisement = AdvertisementService()
    
    @router.get('/', response_model=List[AdvertisementModel], status_code=200)
    async def get_all(self,):
        ...
        
    @router.get('/{uid}', response_model=None, status_code=200)
    async def get_one(self, uid: str):
        ...
    
    @router.post('/create', response_model=AdvertisementCreate, status_code=201)
    async def create(self, advertisement: AdvertisementCreate, db: AsyncSession=Depends(get_session)):
        new_advertisement: Advertisement = await self.advertisement.create(advertisement, db)
        if new_advertisement:
            return HttpResponseCreated({
                "status": "success",
                "data": {
                    "message": "Se ha creado el anuncio satisfactoriamente"
                }
            }).response()
        return HttpResponseBadRequest({
            "status": "fail",
            "data": {
                "message": "No hemos podido crear el anuncio"
            }
        }).response()
    
    @router.put('/update', response_model=None, status_code=201)
    async def update(self):
        ...
    
    @router.patch('/edit', response_model=None, status_code=204)
    async def edit(self):
        ...
    
    @router.delete('/delete/{uid}', response_model=None, status_code=204)
    async def delete(self, uid: str, db: AsyncSession=Depends(get_session)):
        ...
        