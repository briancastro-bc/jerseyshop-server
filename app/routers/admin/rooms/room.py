from fastapi import Depends, Path, Query
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import Room, User
from app.core.http import HttpResponseBadRequest, HttpResponseCreated, HttpResponseNotFound, HttpResponseOK
from app.core.dependency import get_current_user, get_session
from app.common.models import RoomCreate, RoomModel

from .room_service import RoomService

router = InferringRouter()

@cbv(router)
class RoomsController:
    
    def __init__(self) -> None:
        self.room = RoomService()
    
    @router.get('/', response_model=RoomModel, status_code=200)
    async def get_all(self, db: AsyncSession=Depends(get_session)):
        rooms: Room = await self.room.get_all(db)
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
    
    @router.get('/{code}', response_model=RoomModel, status_code=200)
    async def get_by_code(self, code: str=Path(None, title="Get room by code"), db: AsyncSession=Depends(get_session)):
        db_room: Room = await self.room.get_by_code(code, db)
        if db_room:
            return HttpResponseOK({
                "status": "success",
                "data": {
                    "room": db_room
                }
            }).response()
        return HttpResponseNotFound({
            "status": "fail",
            "data": {
                "message": "No se encontró la sala"
            }
        }).response()
    
    @router.post('/create', response_model=RoomCreate, status_code=201)
    async def create(self, room: RoomCreate, db: AsyncSession=Depends(get_session), current_user: User=Depends(get_current_user)):
        room: Room = await self.room.create(room, db, current_user)
        if room:
            return HttpResponseCreated({
                "status": "success",
                "data": {
                    "message": "La sala de soporte ha sido creada",
                    "room": room.code
                }
            }).response()
        return HttpResponseBadRequest({
            "status": "fail",
            "data": {
                "message": "La el nombre de la sala ya es existente"
            }
        }).response()
    
    @router.put('/update/{code}', response_model=RoomModel, status_code=201)
    async def update(self, room: RoomModel, code: str=Path(None, title="Update room by code"), db: AsyncSession=Depends(get_session)):
        pass

    @router.patch('/edit/{code}', response_model=None, status_code=204)
    async def edit(self, code: str=Path(None, title="Edit room by code"), db: AsyncSession=Depends(get_session)):
        pass
    
    @router.delete('/delete/{code}', response_model=None, status_code=204)
    async def delete(self, code: str=Path(None, title="Delete room by code"), db: AsyncSession=Depends(get_session)):
        pass