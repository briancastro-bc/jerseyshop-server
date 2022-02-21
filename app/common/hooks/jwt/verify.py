from fastapi import Depends, HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas import User
from app.core.dependency import get_payload_from_token, get_session

def verify(validate_account: bool=False):
    async def _verify(decoded=Depends(get_payload_from_token), db: AsyncSession=Depends(get_session)):
        if type(decoded) is dict or not decoded:
            raise HTTPException(401, {
                "status": "fail",
                "data": {
                    "message": decoded.get('message') if decoded is not None else 'Token missing'
                }
            })
        if validate_account:
            db_user: User = await db.get(User, decoded['sub'])
            if db_user.is_verify:
                return True
            raise HTTPException(401, {
                "status": "fail",
                "data": {
                    "message": "Verifica tu cuenta para poder acceder"
                }
            })
        return True
    return _verify