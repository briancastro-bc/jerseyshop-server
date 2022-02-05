from typing import Any

from fastapi import Depends, HTTPException, Header

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas import User
from app.common.services import JwtService
from app.database import get_session

def get_access_token(authorization: str=Header(None)):
    access_token: str = authorization.split(' ')[1] if authorization is not None else None
    if not access_token or access_token == 'null':
        return
    decoded = JwtService.decode(access_token, validate=True)
    return decoded

async def get_current_user(token: Any=Depends(get_access_token), db: AsyncSession=Depends(get_session)) -> User:
    if type(token) is dict:
        raise HTTPException(
            401,
            {
                "status": "fail",
                "data": {
                    "message": token.get('message')
                }
            }
        )
    db_current_user: User = await db.get(User, token['sub'])
    return db_current_user