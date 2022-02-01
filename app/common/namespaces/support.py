from typing import Dict, Any
import socketio

class SupportNamespace(socketio.AsyncNamespace):
    
    def __init__(self, namespace=None):
        super().__init__(namespace)
        self.rooms: Dict[str, Any] = {}
    
    async def on_connect(self, sid: str):
        print('User connected: {0}'.format(sid))
    
    async def on_join(self, sid: str, room: str):
        if not room in self.rooms:
            return await self.emit('room_not_found', {
                "message": "Room doesn't exists"
            })
        self.enter_room(sid=sid, room=room)
        await self.emit('user_joined', )
    
    async def on_leave(self):
        ...
        
    async def on_disconnect(self, sid: str):
        print('User disconnected: {0}'.format(sid))