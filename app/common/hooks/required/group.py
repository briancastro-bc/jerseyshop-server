from typing import List

from fastapi import Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas import User
from app.core.dependency import get_current_user
from app.core.schemas import Group, User
from app.database import get_session

def group(code_name: List[str]):
    async def _group(current_user: User=Depends(get_current_user), db: AsyncSession=Depends(get_session)):
        #TODO: Groups validation.
        groups = (await db.scalars(current_user.groups.statement)).all()
        stmt = current_user.groups.statement.where(
            Group.code_name == code_name[0]
        )
        groups_filter = (await db.scalars(stmt)).all()
        print(groups_filter)
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