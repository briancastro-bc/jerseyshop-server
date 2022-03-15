from fastapi import HTTPException, BackgroundTasks, Request, Query, Depends, Body
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import User, Profile, settings
from app.core.dependency import get_session, get_group, Dependency
from app.core.http import HttpResponseBadRequest, HttpResponseCreated, HttpResponseOK, HttpResponseUnauthorized
from app.common.services import JwtService, EmailService, OAuth2Service
from app.common.models import UserCreate, UserBase, UserRecovery, RefreshToken, UserResponseModel
from app.common.helpers import REGISTER_USER_FORMAT, PASSWORD_RECOVERY_FORMAT

from .auth_service import AuthService

import datetime

router = InferringRouter()

@cbv(router)
class AuthController:
    
    def __init__(self) -> None:
        self.email = EmailService()
        self.oauth2 = OAuth2Service(
            provider='google',
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
            client_kwargs={
                'scope': 'openid profile email'
            }
        )
    
    @router.post('/signup', response_model=None, status_code=201)
    async def signup(
        self, 
        user: UserCreate, 
        background_tasks: BackgroundTasks, 
        session: AsyncSession=Depends(Dependency.get_session)
    ):
        new_user: User = await AuthService.create_user(
            user=user,
            session=session
        )
        if new_user:
            access_token: str = JwtService.encode(
                payload={
                    "iss": "jerseyshop.com",
                    "sub": new_user.uid,
                    "iat": datetime.datetime.utcnow(),
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
                },
                encrypt=True
            )
            background_tasks.add_task(
                self.email.send_email, 
                [user.email], 
                "Bienvenido: verifica tu cuenta", 
                message=REGISTER_USER_FORMAT.format(user.name, access_token), 
                format='html'
            )
            return HttpResponseCreated({
                "status": "success",
                "data": {
                    "message": "Gracias por hacer parte de Jersey Shop. Te damos la bienvenida!",
                    "access_token": access_token,
                }
            }).response()
        return HttpResponseBadRequest({
            "status": "fail",
            "data": {
                "message": "El correo electronico ya se encuentra registrado"
            }
        }).response()
        
    @router.post('/login', response_model=None, status_code=200)
    async def login(
        self, 
        user: UserBase, 
        session: AsyncSession=Depends(Dependency.get_session)
    ):
        existented_user: User = await AuthService.verify_user(
            user=user,
            session=session
        )
        if existented_user:
            access_token: str = JwtService.encode(
                payload={
                    "iss": "jerseyshop.com",
                    "sub": existented_user.uid,
                    "iat": datetime.datetime.utcnow(),
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
                },
                encrypt=True
            )
            return HttpResponseOK({
                "status": "success",
                "data": {
                    "access_token": access_token,
                }
            }).response()
        return HttpResponseUnauthorized({
            "status": "fail",
            "data": {
                "message": "Las credenciales de acceso son incorrectas"
            }
        }).response()
    
    @router.get('/google', response_model=None, status_code=200)
    async def google_login(self, request: Request):
        return await self.oauth2.google_login(request)
    
    @router.get('/google/authorize', response_model=None, status_code=200)
    async def google_authorize(self, request: Request, db: AsyncSession=Depends(get_session)):
        google_authorize = await self.oauth2.google_authorize(request)
        if google_authorize:
            query = await db.execute(select(User).where(User.email == google_authorize['email']))
            db_user = query.scalars().first()
            if not db_user:
                new_user = User(
                    email=google_authorize['email'],
                    name=google_authorize['given_name'],
                    last_name=google_authorize['family_name'],
                    birthday=datetime.datetime.utcnow(),
                    accept_advertising=False,
                    accept_terms=True
                )
                new_user_profile = Profile(
                    user_uid=new_user.uid,
                    phone_number="0",
                    photo=google_authorize['picture']
                )
                new_user.profile = new_user_profile
                group = await get_group('users', db)
                db.add(new_user)
                new_user.groups.append(group)
                await db.commit()
            access_token: str = JwtService.encode({
                "iss": google_authorize['iss'],
                "sub": db_user.uid,
                "iat": google_authorize['iat'],
                "exp": google_authorize['exp']
            }, encrypt=True)
            return HttpResponseOK({
                "status": "success",
                "data": {
                    "message": "Te hemos autenticado con Google",
                    "access_token": access_token
                }
            }).response()
        return HttpResponseBadRequest({
            "status": "fail",
            "data": {
                "message": "No pudimos realizar la autenticacion con Google"
            }
        }).response()
    
    @router.get('/verifyAccount', response_model=None, status_code=200)
    async def verify_account(
        cls, 
        token: str=Query(
            None, 
            alias='JWT',
            title='Token',
            description='Token enviado por parametros para verificar al usuario',
        ), 
        session: AsyncSession=Depends(Dependency.get_session)
    ):
        payload = JwtService.decode(encoded=token, validate=False)
        if type(payload) is dict:
            return HttpResponseUnauthorized({
                "status": "fail",
                "data": {
                    "message": payload.get('message')
                }
            }).response()
        verified_user = await AuthService.verify_account(
            payload=payload,
            session=session
        )
        if verified_user:
            return HttpResponseOK({
                "status": "success",
                "data": {
                    "message": "Tu cuenta ha sido verificada"
                }
            }).response()
        return HttpResponseBadRequest({
            "status": "fail",
            "data": {
                "message": "La cuenta ya ha sido verificada"
            }
        }).response()
    
    @router.post('/passwordRecovery', response_model=None, status_code=201)
    async def password_recovery(
        self, 
        user: UserRecovery, 
        background_tasks: BackgroundTasks, 
        session: AsyncSession=Depends(Dependency.get_session)
    ):
        data: dict = await AuthService.password_recovery(
            email=user.email,
            session=session
        )
        if data:
            background_tasks.add_task(
                self.email.send_email,
                [data['user'].email],
                "Recuperación: restablecimiento de contraseña",
                message=PASSWORD_RECOVERY_FORMAT.format(data['user'].name, data['new_password']),
                format='html'
            )
            return HttpResponseCreated({
                "status": "success",
                "data": {
                    "message": "Hemos enviado un email de confirmación"
                }
            }).response()
        return HttpResponseBadRequest({
            "status": "fail",
            "data": {
                "message": "No hay ninguna cuenta registrada con el correo electrónico indicado"
            }
        }).response()
    
    @router.post('/refreshToken', response_model=RefreshToken, status_code=201)
    async def refresh_token(
        self, 
        body=Body(
            ..., 
            title="Access Token",
            description='Access token obtained from the body request'
        )
    ):
        refresh_token = AuthService.refresh_token(body['access_token'])
        if refresh_token:
            return HttpResponseCreated({
                "status": "success",
                "data": {
                    "message": "El token ha sido refrescado",
                    "access_token": refresh_token,
                    "refresh_token": True
                }
            }).response()
        raise HTTPException(
            401,
            {
                "status": "fail",
                "data": {
                    "message": "Token is expired",
                    "refresh_token": False
                }
            }
        )
        