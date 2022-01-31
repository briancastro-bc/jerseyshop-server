from fastapi import Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas import User
from app.common.services import JwtService
from app.database import get_session

async def verify(authorization: str = Header(None), validate_account: bool=True, db: AsyncSession=Depends(get_session)):
    token: str = authorization.split(' ')[1] if authorization is not None else None
    if not token:
        raise HTTPException(401, {
            "status": "fail",
            "data": {
                "message": "Missing Authorization header"
            }
        })
    decoded = JwtService.decode(encoded=token, validate=True)
    if type(decoded) is dict:
        raise HTTPException(401, {
            "status": "fail",
            "data": {
                "message": decoded.get('message')
            }
        })
    if validate_account:
        db_user = await db.query(User).filter_by(uid=decoded['sub']).first()
        if db_user.is_verify:
            return True
        raise HTTPException(401, {
            "status": "fail",
            "data": {
                "message": "Verifica tu cuenta para poder acceder"
            }
        })
    return True