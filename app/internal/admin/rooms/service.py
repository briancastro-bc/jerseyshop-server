from fastapi import HTTPException

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas import Room

from .model import RoomCreate, RoomModel

class RoomService:
    
    def __init__(self) -> None:
        pass
    
    """
        :method get_all - Toma todas las salas de soporte que hayan en la base de datos.
    """
    async def get_all(self, db: AsyncSession):
        query = await db.execute(select(Room).where(Room.is_active == True).order_by(Room.name))
        db_rooms = query.scalars().fetchall()
        if not db_rooms:
            return None
        return db_rooms
    
    """
        :method get_one - Me devuelve una sala de soporte especificada por código.
        :params code - Especifica el codigo de la sala.
    """
    async def get_one(self, code: str, db: AsyncSession):
        query = await db.execute(select(Room).where(Room.code == code))
        db_rooms = query.scalars().first()
        if not db_rooms:
            return None
        return db_rooms
    
    """
        :method create - Permite crear una nueva sala de soporte en la base de datos.
        :param room - Especifica que modelo de datos tendrá una sala en especifico.
    """
    async def create(self, room: RoomCreate, db: AsyncSession):
        query = await db.execute(select(Room).where(Room.name == room.name))
        db_room = query.scalars().first()
        if not db_room:
            room_code: str = self._create_room_code()
            try:
                new_room = Room(
                    code=room_code,
                    name=room.name,
                    limit=room.limit if room.limit is not None else 2
                )
                db.add(new_room)
                await db.commit()
            except Exception as e:
                raise HTTPException(
                    400,
                    {
                        "status": "fail",
                        "data": {
                            "message": "Hubo un error mientras intentabamos crear la sala",
                            "exception": "{0}".format(e)
                        }
                    }
                )
            return new_room
        return None

    """
        :method update - Actualiza los datos de una sala de soporte.
        :param room - Especifica que informacion se quiere actualizar.
    """
    async def update(self, code: str, room: RoomModel, db: AsyncSession):
        try:
            await db.execute(update(Room).where(Room.code == code).values(
                name=room.name,
                limit=room.limit,
                is_active=room.is_active
            ))
            await db.commit()
        except:
            return False
        return True

    """
        :method edit - Edita uno o varios elementos referentes a Room en la base de datos
        :param code - Representa el codigo de la sala.
        :param room_code - En caso de querer editar la sala se pasa el room_code
        :param name - Permite editar el nombre de la sala
        :param limit - Permite editar el limite de la sala.
        :param is_active - Edita el estado de la sala.
    """
    async def edit(self, code: str, db: AsyncSession, **kwargs):
        try:
            await db.execute(update(Room).where(Room.code == code).values(
                code=kwargs.get('room_code'),
                name=kwargs.get('name'),
                limit=kwargs.get('limit'),
                is_active=kwargs.get('is_active'),
            ))
            await db.commit()
        except:
            return False
        return True
    
    """
        :method delete - Borra una sala de soporte de la base de datos
        :param code - El codigo de la sala que se quiere borrar
    """
    async def delete(self, code: str, db: AsyncSession):
        try:
            await db.execute(delete(Room).where(Room.code == code))
            await db.commit()
        except:
            return False
        return True
    
    """
        :func _generate_room_code - Genera un código aleatorio de 8 digitos y los separa a la mitad con un guión.
    """
    def _create_room_code(self):
        import random
        CHARS = 'abcdefghijklmnopqrstuvwxyz'
        room_code: str = ""
        for char in range(8):
            random_char = random.choice(CHARS)
            if char == 4:
                room_code += "-"
            room_code += random_char
        return room_code
        