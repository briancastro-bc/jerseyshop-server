from fastapi import Depends

from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.http import HttpResponseOK, HttpResponseBadRequest
from app.core.schemas import Room
from app.core.dependency import get_session

from app.routers.admin.rooms.room_service import RoomService

router = InferringRouter()

@cbv(router)
class HomeController:
    
    def __init__(self) -> None:
        self.room = RoomService()
    
    @router.get('/rooms', response_model=None, status_code=200)
    async def rooms(self, db: AsyncSession=Depends(get_session)):
        rooms: Room = await self.room.get_all(db)
        if rooms:
            return HttpResponseOK({
                "status": "success",
                "data": {
                    "rooms": rooms
                }
            }).response()
        return HttpResponseBadRequest({
            "status": "fail",
            "data": {
                "message": "No se encontraron salas de soporte"
            }
        }).response()