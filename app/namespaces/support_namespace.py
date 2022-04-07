import socketio
from sqlalchemy import text

from app.core import Room, async_session

class SupportRoomService:
    
    @classmethod
    async def request_rooms_info(
        cls,
    ):
        pass
    
    """
        :classmethod change_room_status - Cambia el estado de la sala entre activo e inactivo.
    """
    @classmethod
    async def change_room_status(
        cls,
        is_active: bool,
        room: str,
    ) -> None:
        async with async_session() as session:
            await session.execute(
                text("UPDATE rooms SET is_active=:is_active WHERE code=:room").\
                    bindparams(
                        is_active=is_active,
                        room=room
                    )
            )
            await session.commit()

"""
    :class SupportNamespace - Representa el espacio de salas de soporte. Endpoint: /support
"""
class SupportNamespace(socketio.AsyncNamespace):
    
    def __init__(self, namespace=None):
        super().__init__(namespace)
        self.rooms: list[str] = []
    
    """
        :event connect - Se emite cuando hay un nuevo socket conectandose.
    """
    async def on_connect(
        self, 
        sid: str, 
        environ: dict[str, object]
    ):
        print(environ)
        print('User connected: {0}'.format(sid))
        await self.save_session(sid, {
            'operating_sys': environ['HTTP_SEC_CH_UA_PLATFORM'],
            'sid': sid
        })
    
    """
        :event create_room - Se emite cuando se crea una nueva sala y agrega la misma a una lista de salas.
        :emit room_exist - En caso de que la sala ya exista.
    """
    async def on_create_room(
        self, 
        sid: str, 
        data: dict[str, object],
    ):
        if data['room'] in self.rooms:
            await self.emit('room_exist', {
                "message": "La sala que intenta crear ya se encuentra activa"
            })
            return
        await SupportRoomService.change_room_status(
            is_active=True,
            room=data['room'],
        )
        self.rooms.append(data['room'])
        await self.save_session(sid, {
            'room': data['room']
        })
        await self.on_join(sid=sid, data=data)
    
    """
        :event join - Se emite cuando alguien se une a una sala.
        :emit room_not_found - En caso de que la sala a la que se intenta acceder no exista.
        :emit message - Cuando detecta que alguien se unio, envia un mensaje a la sala especifica.
    """
    async def on_join(
        self, 
        sid: str, 
        data: dict[str, object], 
    ):
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
    async def on_message(self, sid: str, data: dict[str, object]):
        await self.send({
            "message": data['message'],
        }, room=data['room'])
    
    """
        :event request_rooms - 
    """
    async def on_request_rooms(
        self,
        sid: str,
        data: dict[str, object]
    ):
        rooms: list[Room] = await SupportRoomService.request_rooms_info()
        pass
    
    async def on_new_entry(
        self,
        sid: str,
        data: dict[str, object]
    ):
        async with self.session(sid) as session:
            return await self.emit('notify_entry', {
                "message": "El usuario #{0} accedio a la sala #{1}".format(sid, data['room']),
                "operating_system": session['operating_sys'],
                "system_message": True
            }, room=data['room'])
    
    """
        :event leave - Se emite cuando un usuario abandona la sala en la que se encuentra.
    """
    async def on_leave(self, sid: str, data: dict[str, object]):
        self.leave_room(sid=sid, room=data['room'])
        await self.emit('user_left', room=data['room'])
        await self.send({
            "message": "El usuario # {0} ha salido de la sala".format(sid),
            "system_message": True
        }, room=data['room'])
    
    """
        :event remove_room - Se emite cuando un dueño de sala inactiva la misma.
    """
    async def on_remove_room(self, sid: str, data: dict[str, object]):
        if not data['room'] in self.rooms:
            await self.emit('room_not_found', {
                "message": "La sala no esta activa actualmente"
            })
            return
        self.leave_room(sid=sid, room=data['room'])
        async with self.session(sid) as session:
            await SupportRoomService.change_room_status(
                is_active=False,
                room=session['room']
            )
            await self.close_room(room=session['room'])
            self.rooms.remove(session['room'])
        await self.emit('room_removed', {
            "message": "La sala ha pasado a modo offline"
        })
        
    """
        :event disconnect - Se emite cuando un socket se desconecta.
    """
    async def on_disconnect(self, sid: str):
        print('User disconnected: {0}'.format(sid))