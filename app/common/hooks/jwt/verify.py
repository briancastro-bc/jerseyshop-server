from fastapi import Depends, HTTPException 

from app.core.schemas import User
from app.core.dependency import get_payload_from_token, get_user

def verify(validate_account: bool=False):
    async def _verify(
        decoded: object=Depends(get_payload_from_token), 
        user: User=Depends(get_user(current=True)),
    ):
        if type(decoded) is dict or not decoded:
            raise HTTPException(401, {
                "status": "fail",
                "data": {
                    "message": decoded.get('message') if decoded is not None else 'Token missing'
                }
            })
        if validate_account:
            if user.is_verify:
                return True
            raise HTTPException(401, {
                "status": "fail",
                "data": {
                    "message": "Verifica tu cuenta para poder acceder"
                }
            })
        return True
    return _verify