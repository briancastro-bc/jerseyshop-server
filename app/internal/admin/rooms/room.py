from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

from app.core.http import HttpResponseBadRequest, HttpResponseCreated
from app.core.schemas import Room
from app.database import get_session

from .service import RoomService
from .model import RoomCreate

router = InferringRouter()

@cbv(router)
class RoomsController:
    
    def __init__(self) -> None:
        self.room = RoomService()
    
    @router.get('/', response_model=None, status_code=200)
    async def get_all(self,):
        pass
    
    @router.get('/{code}', response_model=None, status_code=200)
    async def get_one(self, code: str):
        pass
    
    @router.post('/create', response_model=RoomCreate, status_code=201)
    async def create(self, room: RoomCreate, db: AsyncSession=Depends(get_session)):
        room: Room = await self.room.create(room, db)
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
    
    @router.put('/update/{code}', response_model=None, status_code=201)
    async def update(self, code: str):
        pass

    @router.patch('/edit/{code}', response_model=None, status_code=204)
    async def edit(self, code: str):
        pass
    
    @router.delete('/delete/{code}', response_model=None, status_code=204)
    async def delete(self, code: str):
        pass