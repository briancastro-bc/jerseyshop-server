from typing import Any
from fastapi import Depends, Header, HTTPException 
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import User, Group, Permission
from app.core.database import async_session
from app.common.services import JwtService

__all__ = ['dependency']

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
def get_payload_from_token(authorization: str=Header(None)) -> Any:
    access_token: str = authorization.split(' ')[1] if authorization is not None else None
    if not access_token or access_token == 'null':
        return
    decoded = JwtService.decode(access_token, validate=True)
    return decoded

"""
    :function get_current_user - Lee el payload del token y toma el subject del usuario.
    :returns - El usuario encontrado por medio de ese payload.
"""
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

"""
    :function get_group - Consulta los grupos existentes a partir de un codigo de grupo especifico.
    :returns - El grupo encontrado.
"""
async def get_group(code_name: str, db: AsyncSession) -> Group:
    query = await db.execute(select(Group).where(Group.code_name == code_name))
    db_group = query.scalars().first()
    return db_group

class Dependency(object):
    
    @property
    def session(self) -> AsyncSession:
        return self.__session
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        print('Called instance')
        
    @classmethod
    async def get_session(cls) -> AsyncSession:
        async with async_session() as session:
            try:
                yield session
            finally:
                await session.close()
    
    @classmethod
    def get_user(
        cls, 
        current: bool, 
        id: str=None,
    ) -> User:
        async def _get_user():
            if current:
                payload: Any = cls.get_payload()
                if type(payload) is dict or not payload:
                    raise HTTPException(
                        401,
                        {
                            "status": "fail",
                            "data": {
                                "message": payload.get('message') if payload is not None else "Token is missing"
                            }
                        }
                    )
                print(payload['sub'])
                id = payload['sub']
            async with cls.get_session() as session:
                user: User = await session.get(User, id)
                return user
        return _get_user
    
    @classmethod
    def get_payload(
        cls, 
        authorization: str=Header(
            None
        )
    ):
        access_token: str = authorization.split(' ')[1] if authorization is not None else None
        if not access_token or access_token == 'null':
            return
        payload: Any = JwtService.decode(
            encoded=access_token, 
            validate=True
        )
        return payload
        