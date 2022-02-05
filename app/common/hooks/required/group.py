from typing import List

from fastapi import Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas import User
from app.core.dependency import get_current_user
from app.core.schemas import Group, User
from app.database import get_session

def group(code_name: List[str]):
    async def _group(current_user: User=Depends(get_current_user), db: AsyncSession=Depends(get_session)):
        for group in code_name:
            if group in current_user.groups:
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