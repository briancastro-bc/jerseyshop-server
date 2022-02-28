from typing import List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

from app.core import Advertisement
from app.core.http import HttpResponseBadRequest, HttpResponseCreated, HttpResponseNotFound, HttpResponseOK
from app.core.dependency import get_session
from app.common.models import AdvertisementCreate, AdvertisementModel

from .advertisement_service import AdvertisementService

router = InferringRouter()

@cbv(router)
class AdvertisementController:
    
    def __init__(self) -> None:
        self.service = AdvertisementService()
    
    @router.get('/', response_model=AdvertisementModel, status_code=200)
    async def get_all(self, db: AsyncSession=Depends(get_session)):
        advertisements: Advertisement = await self.service.get_all(db)
        if advertisements:
            return HttpResponseOK({
                "status": "success",
                "data": {
                    "advertisements": advertisements
                }
            }).response()
        return HttpResponseNotFound({
            "status": "fail",
            "data": {
                "message": "No se encontraron anuncios"
            }
        }).response()
        
    @router.get('/{uid}', response_model=None, status_code=200)
    async def get_by_id(self, uid: str):
        ...
    
    @router.post('/create', response_model=AdvertisementCreate, status_code=201)
    async def create(self, advertisement: AdvertisementCreate, db: AsyncSession=Depends(get_session)):
        new_advertisement: Advertisement = await self.service.create(advertisement, db)
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
    
    @router.put('/update/{uid}', response_model=None, status_code=201)
    async def update(self, uid: str):
        ...
    
    @router.patch('/edit/{uid}', response_model=None, status_code=204)
    async def edit(self, uid: str):
        ...
    
    @router.delete('/delete/{uid}', response_model=None, status_code=204)
    async def delete(self, uid: str, db: AsyncSession=Depends(get_session)):
        ...
        