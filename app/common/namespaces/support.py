from typing import Dict, Any, List

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas import Room
from app.database import get_session

import socketio

"""
    :class SupportNamespace - Representa el espacio de salas de soporte. Endpoint: /support
"""
class SupportNamespace(socketio.AsyncNamespace):
    
    def __init__(self, namespace=None):
        super().__init__(namespace)
        self.rooms: List[str] = []
    
    """
        :event connect - Se emite cuando hay un nuevo socket conectandose.
    """
    async def on_connect(self, sid: str, environ):
        print('User connected: {0}'.format(sid))
    
    """
        :event create_room - Se emite cuando se crea una nueva sala y agrega la misma a una lista de salas.
        :emit room_exist - En caso de que la sala ya exista.
    """
    async def on_create_room(self, sid: str, data: Dict[str, Any]):
        if data['room'] in self.rooms:
            await self.emit('room_exist', {
                "message": "La sala que intenta crear ya se encuentra activa"
            })
            return
        # Add a new room in the rooms list.
        self.rooms.append(data['room']) 
        await self.on_join(sid=sid, data=data)
    
    """
        :event join - Se emite cuando alguien se une a una sala.
        :emit room_not_found - En caso de que la sala a la que se intenta acceder no exista.
        :emit message - Cuando detecta que alguien se unio, envia un mensaje a la sala especifica.
    """
    async def on_join(self, sid: str, data: Dict[str, Any], db: AsyncSession=Depends(get_session)):
        #db_room: Room = await db.get(Room, data['room'])
        if not data['room'] in self.rooms:
            await self.emit('room_not_found', {
                "message": "La sala de soporte a la que intenta acceder no existe."
            })
            return
        """if db_room.limit > 2:
            await self.emit('room_limit', {
                "message": "El limite de la sala ha sido excedido."
            })
            return
        db_room.limit += 1
        await self.db.commit()"""
        self.enter_room(sid=sid, room=data['room'])
        await self.emit('user_joined', room=data['room'])
        await self.send({
            "message": "El usuario # {0} se unió a la sala".format(sid),
            "system_message": True
        }, room=data['room'])
    
    """
        :event message - Se emite cuando alguna de las dos partes envia un mensaje y devuelve el mismo con los datos.
    """
    async def on_message(self, sid: str, data: Dict[str, Any]):
        await self.send({
            "message": data['message'],
            #"user": sid
        }, room=data['room'])
    
    """
        :event leave - Se emite cuando un usuario abandona la sala en la que se encuentra.
    """
    async def on_leave(self, sid: str, data: Dict[str, Any]):
        ...
    
    """
        :event remove_room - Se emite cuando un dueño de sala inactiva la misma.
    """
    async def on_remove_room(self, sid: str, data: Dict[str, Any]):
        ...
        
    """
        :event disconnect - Se emite cuando un socket se desconecta.
    """
    async def on_disconnect(self, sid: str):
        print('User disconnected: {0}'.format(sid))