from typing import Dict, Any, List

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core import Room
from app.core.dependency import get_session

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
        self.rooms.append(data['room']) 
        await self.on_join(sid=sid, data=data)
    
    """
        :event join - Se emite cuando alguien se une a una sala.
        :emit room_not_found - En caso de que la sala a la que se intenta acceder no exista.
        :emit message - Cuando detecta que alguien se unio, envia un mensaje a la sala especifica.
    """
    async def on_join(self, sid: str, data: Dict[str, Any], db: AsyncSession=Depends(get_session)):
        if not data['room'] in self.rooms:
            await self.emit('room_not_found', {
                "message": "La sala de soporte a la que intenta acceder no existe."
            })
            return
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
        }, room=data['room'])
    
    """
        :event leave - Se emite cuando un usuario abandona la sala en la que se encuentra.
    """
    async def on_leave(self, sid: str, data: Dict[str, Any]):
        self.leave_room(sid=sid, room=data['room'])
        await self.emit('user_left', room=data['room'])
        await self.send({
            "message": "El usuario # {0} ha salido de la sala".format(sid),
            "system_message": True
        }, room=data['room'])
    
    """
        :event remove_room - Se emite cuando un dueño de sala inactiva la misma.
    """
    async def on_remove_room(self, sid: str, data: Dict[str, Any]):
        if not data['room'] in self.rooms:
            await self.emit('room_not_found', {
                "message": "La sala no esta activa actualmente"
            })
            return
        self.leave_room(sid=sid, room=data['room'])
        await self.close_room(room=data['room'])
        self.rooms.remove(data['room'])
        await self.emit('room_removed', {
            "message": "La sala ha sido inactivada"
        })
        
    """
        :event disconnect - Se emite cuando un socket se desconecta.
    """
    async def on_disconnect(self, sid: str):
        print('User disconnected: {0}'.format(sid))