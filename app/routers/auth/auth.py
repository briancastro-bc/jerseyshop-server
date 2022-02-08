from fastapi import Depends, HTTPException

from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.http import HttpResponseBadRequest, HttpResponseCreated, HttpResponseOK, HttpResponseUnauthorized
from app.core.schemas import User
from app.common.services import JwtService, EmailService
from app.common.models import UserCreate, UserBase, UserRecovery, RefreshToken
from app.database import get_session

from .service import AuthService

import datetime

router: InferringRouter = InferringRouter()

@cbv(router)
class AuthController:
    
    def __init__(self) -> None:
        self.auth = AuthService()
        self.email = EmailService()
        self.message_format = """
            <center>
                <div style="padding: 0%;
                margin: 0%;
                width: 75%;
                height: 100%;
                border:1px solid rgba(0,0,0,0.25);
                padding: 24px;
                border-radius: 25px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;"
                >
                <img style="width: 75%;
                            float: left;
                            margin-left: 16%;"
                src="https://i.imgur.com/ezOUjf5.png" alt="Company logo">
                <br style="clear: both;">
                <center>
                <h1 style="font-weight: 400;">Hola <strong>{0}</strong></h1> <h2 style="font-weight: 400; font-size:24px;"><br>¡Gracias por registrarte en Jersey Shop!</h2>
                <h2 style="font-weight: 400;">Sólo falta un último paso, y, con esto, podrás acceder a las <strong>compras online</strong> y <strong>contenido único para tí</strong> <br><br><a
                    style="color: white;
                        padding: 10px;
                        border-radius: 50px;
                        background-color: rgb(10, 137, 255);
                        font-style: none;
                        text-decoration: none;
                        font-size: 1.3rem;"
                    href="http://localhost:8000/auth/verifyAccount?token={1}">Verificar cuenta</a>
                </h2>
                </center>
            </div>
            </center>
        """
    
    @router.post('/signup', response_model=UserCreate, status_code=201)
    async def signup(self, user: UserCreate, db: AsyncSession=Depends(get_session)):
        db_user: User = await self.auth.register(user, db)
        if db_user is None:
            return HttpResponseBadRequest({
                "status": "fail",
                "data": {
                    "message": "El correo electronico ya se encuentra registrado"
                }
            }).response()
        access_token: str = JwtService.encode(
            payload={
                "iss": "jerseyshop.com",
                "sub": db_user.uid,
                "iat": datetime.datetime.utcnow(),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
            },
            encrypt=True
        )
        await self.email.send_email([user.email], "Bienvenido: verifica tu cuenta", message=self.message_format.format(user.name, access_token), format='html')
        return HttpResponseCreated({
            "status": "success",
            "data": {
                "message": "Gracias por hacer parte de Jersey Shop. Te damos la bienvenida!",
                "access_token": access_token,
                "user": db_user
            }
        }).response()
        
    @router.post('/login', response_model=UserBase, status_code=200)
    async def login(self, user: UserBase, db: AsyncSession=Depends(get_session)):
        db_user: User = await self.auth.login(user, db)
        if db_user is None:
            return HttpResponseUnauthorized({
                "status": "fail",
                "data": {
                    "message": "Las credenciales de acceso son incorrectas"
                }
            }).response()
        access_token: str = JwtService.encode(
            payload={
                "iss": "jerseyshop.com",
                "sub": db_user.uid,
                "iat": datetime.datetime.utcnow(),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
            },
            encrypt=True
        )
        return HttpResponseOK({
            "status": "success",
            "data": {
                "access_token": access_token,
                "user": db_user
            }
        }).response()
    
    @router.get('/verifyAccount', status_code=200)
    async def verify_account(self, token: str, db: AsyncSession=Depends(get_session)):
        decoded = JwtService.decode(encoded=token, validate=True)
        if type(decoded) is dict:
            return HttpResponseUnauthorized({
                "status": "fail",
                "data": {
                    "message": decoded.get('message')
                }
            }).response()
        db_user = await self.auth.verify_account(decoded, db)
        if db_user:
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
    
    @router.post('/passwordRecovery', status_code=201)
    async def password_recovery(self, user: UserRecovery, db: AsyncSession=Depends(get_session)):
        user: list = await self.auth.password_recovery(email=user.email, db=db)
        if user is None:
            return HttpResponseBadRequest({
                "status": "fail",
                "data": {
                    "message": "No hay ninguna cuenta registrada con el correo electrónico indicado"
                }
            }).response()
        message_format = """
                <center>
                    <div style="padding: 0%;
                    margin: 0%;
                    width: 75%;
                    height: 100%;
                    border:1px solid rgba(0,0,0,0.25);
                    padding: 24px;
                    border-radius: 25px;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;"
                    >
                    <img style="width: 75%;
                                float: left;
                                margin-left: 16%;"
                    src="https://i.imgur.com/ezOUjf5.png" alt="Company logo">
                    <br style="clear: both;">
                    <center>
                    <h1 style="font-weight: 400;">Hola <strong>{0}</strong></h1> <h2 style="font-weight: 400; font-size:24px;"><br>¿Parece que intentas recuperar tú contraseña?</h2>
                    <h2 style="font-weight: 400;">A continuación, creamos una nueva para tí <br><br>
                        <span
                        style="color: white;
                            padding: 10px;
                            border-radius: 0;
                            background-color: rgb(10, 137, 255);
                            font-style: none;
                            text-decoration: none;
                            font-size: 1.3rem;"
                        ">{1}</span>
                    </h2>
                    </center>
                </div>
                </center>
            """.format(user[0].name, user[1])
        await self.email.send_email([user[0].email], "Recuperación: restablecimiento de contraseña", message=message_format, format='html')
        return HttpResponseCreated({
            "status": "success",
            "data": {
                "message": "Hemos enviado un email de confirmación"
            }
        }).response()
    
    @router.post('/refreshToken', response_model=RefreshToken, status_code=201)
    async def refresh_token(self, token: RefreshToken):
        refresh_token = self.auth.refresh_token(access_token=token.access_token)
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
        