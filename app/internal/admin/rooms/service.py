from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas import Room

from .model import RoomCreate

class RoomService:
    
    def __init__(self) -> None:
        pass
    
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
        