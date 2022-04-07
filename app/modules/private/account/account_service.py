from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import User, Profile

class AccountService:
    
    """
        :classmethod get_user_data - Toma toda la informacion de la cuenta del usuario.
        :param user - El usuario especifico del cual se quiere mostrar la informacion.
    """
    @classmethod
    async def get_user_data(
        cls, 
        user: User, 
        session: AsyncSession
    ) -> User:
        try:
            result = await session.execute(
                select(User).where(
                    User.uid == user.uid
                ).join(Profile)
            )
            user = result.scalars().first()
            return user
        except Exception as e:
            raise HTTPException(
                400,
                {
                    "status": "fail",
                    "data": {
                        "message": "No pudimos mostrar los datos de tu cuenta"
                    }
                }
            )