from fastapi import Depends
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import Advertisement, Room
from app.core.dependency import get_session, Dependency
from app.core.http import HttpResponseNotFound, HttpResponseOK
from app.common.models import AdvertisementModel

from app.routers.admin.advertisement.advertisement_service import AdvertisementService
from app.routers.admin.rooms.room_service import RoomService

router = InferringRouter()

@cbv(router)
class RootController:
    
    def __init__(self) -> None:
        self.rooms_service = RoomService()
    
    @router.get('/advertisements', response_model=AdvertisementModel, status_code=200)
    async def advertisements(
        self, 
        session: AsyncSession=Depends(Dependency.get_session)
    ):
        advertisements: list[Advertisement] = await AdvertisementService.get_all_public(
            session=session
        )
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
    
    @router.get('/rooms', response_model=None, status_code=200)
    async def rooms(self, db: AsyncSession=Depends(get_session)):
        rooms: Room = await self.rooms_service.get_all(db)
        if rooms:
            return HttpResponseOK({
                "status": "success",
                "data": {
                    "rooms": rooms
                }
            }).response()
        return HttpResponseNotFound({
            "status": "fail",
            "data": {
                "message": "No se encontraron salas de soporte"
            }
        }).response()