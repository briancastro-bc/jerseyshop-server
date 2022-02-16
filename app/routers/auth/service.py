from fastapi import HTTPException

from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.common.models import UserCreate, UserBase
from app.common.services import JwtService
from app.core.schemas import User, Group, Profile

import time, datetime

class AuthService:
    
    def __init__(self) -> None:
        self.__password_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    """
        :method register - Crea un nuevo usuario en la base de datos pasandole un perfil
        asociado a ese nuevo usuario.
    """
    async def register(self, user: UserCreate, db: AsyncSession):
        query = await db.execute(select(User).where(User.email == user.email))
        db_user = query.scalars().first()
        if not db_user or db_user is None:
            hash_password: str = self._get_password_hash(user.password)
            try:
                new_user = User(
                    email=user.email, 
                    password=hash_password, 
                    name=user.name, 
                    last_name=user.last_name, 
                    birthday=user.birthday, 
                    accept_advertising=user.accept_advertising, 
                    accept_terms=user.accept_terms
                )
                new_user_profile = Profile(
                    user_uid=new_user.uid,
                    phone_number="1234567890",
                    photo="https://www.pngarts.com/files/3/Avatar-PNG-Pic.png"
                )
                new_user.profile = new_user_profile
                query_group = await db.execute(select(Group).where(Group.code_name == 'users'))
                db_group = query_group.scalars().first()
                db.add(new_user)
                #TODO: Resolve groups and permissions validation.
                new_user.groups.append(db_group)
                await db.commit()
                return new_user
            except Exception as e:
                raise HTTPException(status_code=400, detail={
                    "status": "fail",
                    "data": {
                        "message": "Ocurrio un error",
                        "exception": "{}".format(e)
                    }
                })
        return None
    
    async def login(self, user: UserBase, db: AsyncSession):
        query = await db.execute(select(User).where(User.email == user.email))
        db_user = query.scalars().first()
        if db_user:
            verify_password = self._verify_password(user.password, db_user.password)
            if verify_password:
                return db_user
            return None
        return None
    
    async def verify_account(self, decoded, db: AsyncSession):
        db_user: User = await db.get(User, decoded['sub'])
        if db_user:
            if not db_user.is_verify:
                db_user.is_verify = True
                await db.commit()
                return db_user
            return None
        return HTTPException(401, {
            "status": "fail",
            "data": {
                "message": "La cuenta del usuario es inválida o no existe"
            }
        })
        
    async def password_recovery(self, email: str, db: AsyncSession):
        query = await db.execute(select(User).where(User.email == email))
        db_user: User = query.scalars().first()
        if db_user:
            new_password: str = self._create_new_password()
            hash_password = self._get_password_hash(new_password)
            db_user.password = hash_password
            await db.commit()
            return [db_user, new_password]
        return None
        
    def refresh_token(self, access_token: str):
        decoded = JwtService.decode(encoded=access_token, validate=True)
        if type(decoded) is dict:
            return None
        if decoded['exp'] <= time.time() + 600:
            new_token: str = JwtService.encode(
                payload={
                    "iss": "jerseyshop.com",
                    "sub": decoded['sub'],
                    "iat": datetime.datetime.utcnow(),
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
                },
                encrypt=True
            )
            return new_token
        return access_token
    
    def _get_password_hash(self, password: str):
        return self.__password_ctx.hash(password)
    
    def _verify_password(self, plain_password: str or bytes, h_password: str or bytes):
        return self.__password_ctx.verify(plain_password, h_password)
    
    def _create_new_password(self, password_lenght: int=8):
        import random
        CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@~+-*"
        new_password: str = ""
        for i in range(password_lenght):
            rand_choice: str = random.choice(CHARACTERS)
            new_password += rand_choice
        return new_password