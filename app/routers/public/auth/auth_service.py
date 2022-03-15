from typing import Any
from fastapi import HTTPException
from sqlalchemy import select, insert, text
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.core import User, Group, Profile
from app.common.models import UserCreate, UserBase
from app.common.services import JwtService
from app.core.dependency import get_group

import time, datetime

class AuthService:
    
    __password_ctx__ = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto"
    )
    
    """
        :classmethod create_user - Crea un nuevo usuario en la base de datos pasandole un perfil
        asociado a ese nuevo usuario.
        :param user - Representa el objeto del nuevo usuario que se creara.
    """
    @classmethod
    async def create_user(
        cls, 
        user: UserCreate, 
        session: AsyncSession
    ) -> User:
        result = await session.execute(
            text('SELECT email FROM users WHERE email = :email').\
            bindparams(email=user.email)
        )
        existented_user = result.first()
        if not existented_user:
            encrypted_password: str = cls._get_password_hash(user.password)
            try:
                new_user = User(
                    email=user.email, 
                    password=encrypted_password, 
                    name=user.name, 
                    last_name=user.last_name, 
                    birthday=user.birthday, 
                    accept_advertising=user.accept_advertising, 
                    accept_terms=user.accept_terms
                )
                new_user_profile = Profile(
                    user_uid=new_user.uid,
                    phone_number=user.profile.phone_number,
                    gender=user.profile.gender,
                    photo="https://www.pngarts.com/files/3/Avatar-PNG-Pic.png"
                )
                new_user.profile = new_user_profile
                group = await get_group('users', session)
                session.add(new_user)
                new_user.groups.append(group)
                await session.commit()
                return new_user
            except Exception as e:
                raise HTTPException(
                    400,
                    {
                    "status": "fail",
                    "data": {
                        "message": "No se pudo registrar el usuario",
                    }
                })
        return None
    
    """
        :classmethod verify_user - Verifica al usuario que este intentando ingresar
        :param user - El objeto de usuario que intenta iniciar sesion
    """
    @classmethod
    async def verify_user(
        cls, 
        user: UserBase, 
        session: AsyncSession
    ) -> User:
        result = await session.execute(
            select(User).where(
                User.email == user.email
            )
        )
        existented_user: User = result.scalars().first()
        if existented_user:
            verify_password: bool = cls._verify_password(user.password, existented_user.password)
            if verify_password:
                return existented_user
            return False
        return None
    
    """
        :classmethod verify_account - Verifica una cuenta de usuario apartir de un payload.
        :param decoded - Determina el payload almacenado por el usuario
    """
    @classmethod
    async def verify_account(
        cls, 
        payload: Any, 
        session: AsyncSession
    ) -> User:
        user: User = await session.get(User, payload['sub'])
        if user:
            if not user.is_verify:
                user.is_verify = True
                await session.commit()
                return user
            return None
        raise HTTPException({
            400,
            {
                "status": "fail",
                "data": {
                    "message": "La cuenta de usuario es invalida o no existe"
                }
            }
        })
    
    """
        :classmethod password_recovery - Valida si un usuario existe y en dado caso, le asigna una nueva contrasena
        :param email - El email del posible usuario
    """
    @classmethod
    async def password_recovery(
        cls, 
        email: str, 
        session: AsyncSession
    ):
        result = await session.execute(
            select(User).where(
                User.email == email
            )
        )
        user: User = result.scalars().first()
        if user:
            new_password: str = cls._create_new_password()
            encrypted_password = cls._get_password_hash(new_password)
            user.password = encrypted_password
            await session.commit()
            return dict(user=user, new_password=new_password)
        return None
        
    """
        :classmethod refresh_token - Refresca el token de acceso JWT.
        :param access_token - El token actual que tiene el usuario.
    """
    @classmethod
    def refresh_token(
        cls, 
        access_token: str
    ):
        payload = JwtService.decode(encoded=access_token, validate=True)
        if type(payload) is dict:
            return None
        if payload['exp'] <= time.time() + 600:
            new_token: str = JwtService.encode(
                payload={
                    "iss": "jerseyshop.com",
                    "sub": payload['sub'],
                    "iat": datetime.datetime.utcnow(),
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
                },
                encrypt=True
            )
            return new_token
        return access_token
    
    """
        :classmethod _get_password_hash - Retorna una nueva contraseña encriptada a partir de un texto plano.
        :param password - La contrasena en texto plano a encriptar
        :returns - La contrasena encriptada.
    """
    @classmethod
    def _get_password_hash(cls, password: str) -> str:
        return cls.__password_ctx__.hash(password)
    
    """
        :classmehtod _verify_password - Valida si un texto plano coincide con una contrasena encriptada
        :param plain_password - Contrasena en texto plano
        :param encrypted_password - Contrasena encriptada
        :returns True - Si coinciden, de lo contrario False.
    """
    @classmethod
    def _verify_password(
        cls, 
        plain_password: str or bytes, 
        encrypted_password: str or bytes
    ) -> bool:
        return cls.__password_ctx__.verify(
            plain_password, 
            encrypted_password
        )
    
    """
        :classmethod _create_new_password - Crea una nueva contrasena con caracteres aleatorios
        :param password_length - Determina la cantidad de caracteres que tendra la contrasena
        :returns - La nueva contrasena generada
    """
    @classmethod
    def _create_new_password(cls, password_length: int=8):
        import random
        CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@~+-*"
        new_password: str = ""
        for i in range(password_length):
            rand_choice: str = random.choice(CHARACTERS)
            new_password += rand_choice
        return new_password