from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import User, Group
from app.core.dependency import get_current_user, get_session

def group(code_name: List[str]):
    async def _group(current_user: User=Depends(get_current_user), db: AsyncSession=Depends(get_session)):
        query_groups = await db.execute(select(Group).where(Group.code_name == code_name))
        db_groups = query_groups.scalars().first()
        for i in range(len(code_name)): # TODO: Parcially works
            if current_user.groups[i] == db_groups:
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