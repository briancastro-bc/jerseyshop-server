from fastapi import Header, Response, HTTPException

from app.common.services import JwtService

import time, datetime

"""
    :dependency refresh - Verifica si el token que se envia por cabecera esta a punto de expirar, de ser asi
    genera un nuevo token JWT y lo envia en la cabecera. En caso de que no haya expirado continúa con la solicitud.
"""
def refresh(authorization: str=Header(None)):
    current_token: str = authorization.split(' ')[1] if authorization is not None else None
    if not current_token or current_token == 'null':
        return
    decoded = JwtService.decode(encoded=current_token, validate=True)
    # Si es ejecutada esta exception quiere decir que el token expiró.
    if type(decoded) is dict:
        raise HTTPException(
            # Capturar este 401 en el lado del frontend y verificar si la clave refresh_token esta en false
            # de esta manera me doy cuenta si vención el token.
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
        """response = Response(
            {
                "status": "success",
                "data": {
                    "message": "Access token was refreshed",
                    "access_token": new_token,
                    "refresh_token": True
                }
            },
            status_code=200
        )
        return response"""
    return