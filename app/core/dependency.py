from typing import Any

from fastapi import Depends, HTTPException, Header

from sqlalchemy.ext.asyncio import AsyncSession

from app.core import User
from app.core.database import async_session
from app.common.services import JwtService

async def get_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
        
def get_payload_from_token(authorization: str=Header(None)):
    access_token: str = authorization.split(' ')[1] if authorization is not None else None
    if not access_token or access_token == 'null':
        return
    decoded = JwtService.decode(access_token, validate=True)
    return decoded

async def get_current_user(decoded: Any=Depends(get_payload_from_token), db: AsyncSession=Depends(get_session)) -> User:
    if type(decoded) is dict or not decoded:
        raise HTTPException(
            401,
            {
                "status": "fail",
                "data": {
                    "message": decoded.get('message') if decoded is not None else 'Token is missing'
                }
            }
        )
    db_current_user: User = await db.get(User, decoded['sub'])
    return db_current_user