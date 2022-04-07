from fastapi import Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import User, Group, Permission
from app.core.database import async_session
from app.common.services import JwtService

"""
    :function get_session - Genera una nueva sesion de la base de datos.
"""
async def get_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

"""
    :function get_payload_from_token - Se encarga de leer la cabecera del token y lee la misma para obtenerlo
    :returns - El payload del token en caso de no ser None.
"""
def get_payload_from_token(authorization: str=Header(None)) -> object:
    access_token: str = authorization.split(' ')[1] if authorization is not None else None
    if not access_token or access_token == 'null':
        return
    payload = JwtService.decode(access_token, validate=True)
    return payload

"""
    :function get_current_user - Lee el payload del token y toma el subject del usuario.
    :returns - El usuario encontrado por medio de ese payload.
"""
def get_user(current: bool) -> User:
    async def _get_user(
        payload: object=Depends(get_payload_from_token), 
        session: AsyncSession=Depends(get_session)
    ):
        if type(payload) is dict or not payload:
            raise HTTPException(
                401,
                {
                    "status": "fail",
                    "data": {
                        "message": payload.get('message') if payload is not None else 'Token is missing'
                    }
                }
            )
        if current:
            user: User = await session.get(User, payload['sub'])
            return user
        pass
    return _get_user

"""
    :function get_group - Consulta los grupos existentes a partir de un codigo de grupo especifico.
    :returns - El grupo encontrado.
"""
async def get_group(
    code_name: str, 
    session: AsyncSession
) -> Group:
    result = await session.execute(
        select(Group).where(Group.code_name == code_name)
    )
    group = result.scalars().first()
    return group