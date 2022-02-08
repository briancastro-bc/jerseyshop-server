from typing import Dict, Any, Optional, List

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session

import socketio

class SupportNamespace(socketio.AsyncNamespace):
    
    def __init__(self, namespace=None, db: AsyncSession=Depends(get_session)):
        super().__init__(namespace)
        self.rooms: List[str] = []
        self.rooms_limit: int = 2
    
    async def on_connect(self, sid: str, environ):
        print('User connected: {0}'.format(sid))
    
    async def on_create_room(self, sid: str, data: Dict[str, Any]):
        if len(self.rooms) > self.rooms_limit:
            await self.emit('room_limit', {
                "message": "El limite de la sala de soporte fue superado."
            })
            return
        # Add a new room in the rooms list.
        self.rooms.append(data['room']) 
        await self.on_join(sid=sid, data=data)
    
    async def on_join(self, sid: str, data: Dict[str, Any]):
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
    
    async def on_message(self, sid: str, data: Dict[str, Any]):
        await self.send({
            "message": data['message'],
            #"user": sid
        }, room=data['room'])
    
    async def on_leave(self, sid: str, data: Dict[str, Any]):
        ...
        
    async def on_disconnect(self, sid: str):
        print('User disconnected: {0}'.format(sid))