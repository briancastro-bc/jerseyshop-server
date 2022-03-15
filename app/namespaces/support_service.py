from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependency import Dependency

class SupportRoomService:
    
    @classmethod
    async def request_rooms_info(
        cls,
        session: AsyncSession=Depends(Dependency.get_session)
    ):
        pass