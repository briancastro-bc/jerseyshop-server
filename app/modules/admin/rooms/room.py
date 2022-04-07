from fastapi import Depends, Path, Query
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession

from .room_service import RoomService

from app.core import Room, User
from app.core.http_responses import HttpResponseBadRequest, HttpResponseCreated, HttpResponseNotFound, HttpResponseOK
from app.core.dependency import get_session, get_user
from app.common.models import RoomCreate, RoomModel

router = InferringRouter()

@cbv(router)
class RoomsController:
    
    @router.get('/', response_model=RoomModel, status_code=200)
    async def get_all(
        self,
        order_by: int|None=Query(
            2,
            title='Ordenamiento',
            description='Forma en la que se ordenaran las salas'
        ),
        session: AsyncSession=Depends(get_session)
    ):
        rooms: list[Room] = await RoomService.get_all_protected(
            order_by=order_by,
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
    
    @router.get('/{code}', response_model=RoomModel, status_code=200)
    async def get_by_code(
        self, 
        code: str=Path(
            None, 
            title='By code',
            description='Get room by code'
        ), 
        session: AsyncSession=Depends(get_session)
    ):
        room: Room = await RoomService.get_by_code(
            code=code,
            session=session
        )
        if room:
            return HttpResponseOK({
                "status": "success",
                "data": {
                    "room": room
                }
            }).response()
        return HttpResponseNotFound({
            "status": "fail",
            "data": {
                "message": "No se encontró la sala"
            }
        }).response()
    
    @router.post('/create', response_model=RoomCreate, status_code=201)
    async def create(
        self, 
        room: RoomCreate, 
        current_user: User=Depends(get_user(
            current=True
        )),
        session: AsyncSession=Depends(get_session), 
    ):
        new_room: Room = await RoomService.create_one(
            room=room,
            current_user=current_user,
            session=session
        )
        if new_room:
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
    
    @router.put('/{code}', response_model=RoomModel, status_code=201)
    async def update(self, room: RoomModel, code: str=Path(None, title="Update room by code"), db: AsyncSession=Depends(get_session)):
        pass

    @router.patch('/{code}', response_model=None, status_code=204)
    async def edit(self, code: str=Path(None, title="Edit room by code"), db: AsyncSession=Depends(get_session)):
        pass
    
    @router.delete('/{code}', response_model=None, status_code=204)
    async def delete(self, code: str=Path(None, title="Delete room by code"), db: AsyncSession=Depends(get_session)):
        pass