from fastapi import Depends
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import Advertisement, Room
from app.core.http_responses import HttpResponseNotFound, HttpResponseOK
from app.core.dependency import get_session
from app.common.models import AdvertisementModel, RoomModel
from app.modules.admin.advertisement.advertisement_service import AdvertisementService
from app.modules.admin.rooms.room_service import RoomService

router = InferringRouter()

@cbv(router)
class RootController:
    
    @router.get('/advertisements', response_model=AdvertisementModel, status_code=200)
    async def advertisements(
        self, 
        session: AsyncSession=Depends(get_session)
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
    
    @router.get('/rooms', response_model=RoomModel, status_code=200)
    async def rooms(
        self, 
        session: AsyncSession=Depends(get_session)
    ):
        rooms: Room = await RoomService.get_all_public(
            session=session
        )
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