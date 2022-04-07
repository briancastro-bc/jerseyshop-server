from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import User, Group
from app.core.dependency import get_user, get_session

def group(code_name: list[str]):
    async def _group(
        current_user: User=Depends(get_user(current=True)), 
        session: AsyncSession=Depends(get_session)
    ) -> Group:
        result = await session.execute(
            select(Group).where(Group.code_name == code_name)
        )
        groups = result.scalars().first()
        for i in range(len(code_name)): # TODO: Parcially works
            if current_user.groups[i] == groups:
                return
        raise HTTPException(
            403,
            {
                "status": "fail",
                "data": {
                    "message": "El usuario no pertenece al grupo requerido"
                }
            }
        )
    return _group