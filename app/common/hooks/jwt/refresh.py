from fastapi import Depends, HTTPException

from app.core.dependency import get_payload_from_token
from app.common.services import JwtService

import time, datetime

"""
    :dependency refresh - Verifica si el token que se envia por cabecera esta a punto de expirar, de ser asi
    genera un nuevo token JWT y lo envia en la cabecera. En caso de que no haya expirado continúa con la solicitud.
"""
def refresh(decoded=Depends(get_payload_from_token)):
    if type(decoded) is dict:
        raise HTTPException(
            401,
            {
                "status": "fail",
                "data": {
                    "message": decoded.get('message'),
                    "refresh_token": False
                }
            }
        )
    if decoded['exp'] >= time.time() + 600:
        new_token: str = JwtService.encode(
            payload={
                "iss": "jerseyshop.com",
                "sub": decoded['sub'],
                "iat": datetime.datetime.utcnow(),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
            },
            encrypt=True
        )
        raise HTTPException(
            401,
            {
                "status": "success",
                "data": {
                    "message": "Access token was refresh",
                    "access_token": new_token,
                    "refresh_token": True
                }
            }
        )
    return