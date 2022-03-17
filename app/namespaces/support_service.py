from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session

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