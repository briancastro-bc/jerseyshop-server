from fastapi import HTTPException
from sqlalchemy import delete, select, update, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import Room, User
from app.common.models import RoomCreate, RoomModel, RoomUpdatePartial

class RoomService:
    
    """
        :method get_all_public - Toma todas las salas de soporte que hayan en la base de datos.
    """
    @classmethod
    async def get_all_public(
        cls,
        session: AsyncSession
    ) -> list[Room]:
        try:
            result = await session.execute(
                select(Room).where(
                    Room.is_active == True
                ).order_by(Room.name)
            )
            rooms = result.unique().scalars().fetchall()
            return rooms
        except Exception as e:
            return None
    
    @classmethod
    async def get_all_protected(
        cls,
        order_by: int,
        session: AsyncSession
    ) -> list[Room]:
        try:
            result = await session.execute(
                text('SELECT * FROM rooms ORDER BY :order_by').\
                    bindparams(order_by=order_by)
            )           
            rooms: list[Room] = result.all()
            return rooms
        except Exception as e:
            raise HTTPException(
                400,
                {
                    "status": "fail",
                    "data": {
                        "message": "No pudimos mostrar las salas disponibles"
                    }
                }
            )

    """
        :method get_one - Me devuelve una sala de soporte especificada por código.
        :params code - Especifica el codigo de la sala.
    """
    @classmethod
    async def get_by_code(
        cls, 
        code: str, 
        session: AsyncSession
    ) -> Room:
        try:
            result = await session.execute(
                select(Room).where(
                    Room.code == code
                )
            )
            room = result.scalars().first()
            return room
        except Exception:
            return None
    
    """
        :method create_one - Permite crear una nueva sala de soporte en la base de datos.
        :param room - Especifica que modelo de datos tendrá una sala en especifico.
    """
    @classmethod
    async def create_one(
        cls, 
        room: RoomCreate, 
        current_user: User,
        session: AsyncSession
    ) -> Room:
        result = await session.execute(
            select(Room).where(
                Room.name == room.name
            )
        )
        existented_room = result.scalars().first()
        if not existented_room:
            room_code: str = cls._create_room_code()
            try:
                new_room = Room(
                    code=room_code,
                    name=room.name,
                    limit=room.limit if room.limit is not None else 2,
                    owner=current_user.uid
                )
                session.add(new_room)
                await session.commit()
                return new_room
            except Exception as e:
                raise HTTPException(
                    400,
                    {
                        "status": "fail",
                        "data": {
                            "message": "Hubo un error mientras intentabamos crear la sala"
                        }
                    }
                )
        return None

    """
        :method update - Actualiza los datos de una sala de soporte.
        :param room - Especifica que informacion se quiere actualizar.
    """
    async def update(self, code: str, room: RoomModel, db: AsyncSession):
        try:
            updated_room = await db.execute(
                update(Room)
                .values(**room.dict())
                .where(Room.code == code)
            )
            await db.commit()
            return updated_room
        except Exception:
            return None

    """
        :method edit - Edita uno o varios elementos referentes a Room en la base de datos
        :param code - Representa el codigo de la sala.
        :param room_code - En caso de querer editar la sala se pasa el room_code
        :param name - Permite editar el nombre de la sala
        :param limit - Permite editar el limite de la sala.
        :param is_active - Edita el estado de la sala.
    """
    async def edit(self, code: str, room: RoomUpdatePartial, db: AsyncSession):
        try:
            await db.execute(
                update(Room)
                .values(**room.dict(
                    exclude_unset=True
                ))
                .where(Room.code == code)
            )
            await db.commit()
        except Exception:
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
            return True
        except Exception:
            return None
    
    """
        :func _generate_room_code - Genera un código aleatorio de 8 digitos y los separa a la mitad con un guión.
    """
    @classmethod
    def _create_room_code(cls):
        import random
        CHARS = 'abcdefghijklmnopqrstuvwxyz'
        room_code: str = ""
        for char in range(8):
            random_char = random.choice(CHARS)
            if char == 4:
                room_code += "-"
            room_code += random_char
        return room_code
        