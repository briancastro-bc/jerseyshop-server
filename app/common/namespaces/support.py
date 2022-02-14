from typing import Dict, Any, Optional, List

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas import Room
from app.database import get_session

import socketio

class SupportNamespace(socketio.AsyncNamespace):
    
    def __init__(self, namespace=None):
        super().__init__(namespace)
        self.rooms: List[str] = []
    
    async def on_connect(self, sid: str, environ):
        print('User connected: {0}'.format(sid))
    
    async def on_create_room(self, sid: str, data: Dict[str, Any]):
        if data['room'] in self.rooms:
            await self.emit('room_exist', {
                "message": "La sala que intenta crear ya se encuentra activa"
            })
            return
        # Add a new room in the rooms list.
        self.rooms.append(data['room']) 
        await self.on_join(sid=sid, data=data)
    
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
    
    async def on_message(self, sid: str, data: Dict[str, Any]):
        await self.send({
            "message": data['message'],
            #"user": sid
        }, room=data['room'])
    
    async def on_leave(self, sid: str, data: Dict[str, Any]):
        ...
        
    async def on_disconnect(self, sid: str):
        print('User disconnected: {0}'.format(sid))