from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import User, Profile

class AccountService:
    
    def __init__(self) -> None:
        pass
    
    async def my_account(self, user: User, db: AsyncSession):
        try:
            query = await db.execute(select(User).where(User.uid == user.uid).join(Profile))
            current_user = query.scalars().first()
            if current_user:
                return current_user
            return None
        except Exception:
            raise Exception