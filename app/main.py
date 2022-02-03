from typing import Any

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.common.namespaces import ChatNamespace, SupportNamespace
from app.common.services import JwtService
from app.common.hooks import jwt
from app.database import database, init_models

from app.routers import auth, home
from app.internal import admin

import socketio, time, datetime

def create_application():
    
    _app = FastAPI(
        debug=True,
        title=settings.PROJECT_NAME,
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    """
        :middleware refresh_token - Verifica si el token que se envia por cabecera esta a punto de expirar, de ser asi
        genera un nuevo token JWT y lo envia en la cabecera.
    """
    @_app.middleware('http')
    async def refresh_token(request: Request, call_next: Any):
        response = await call_next(request)
        authorization = request.headers.get('Authorization').split(' ')[1] if request.headers.get('Authorization') else "default"
        current_token: str = authorization
        decoded = JwtService.decode(encoded=current_token, validate=True)
        # Token is expired
        if type(decoded) is dict:
            return response
        # Token will expire soon. It going to refresh.
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
            response.headers['Authorization'] = "Bearer {}".format(new_token)
            return response
        return response
    
    return _app

io = socketio.AsyncServer(logger=True, cors_allowed_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS], async_mode='asgi', ping_timeout=30000, always_connect=True)
app = create_application()
io_app = socketio.ASGIApp(io, app)

@app.on_event('startup')
async def startup():
    await init_models()
    await database.connect()
    
@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

app.include_router(router=home.router)
app.include_router(router=auth.router, prefix='/auth')
app.include_router(
    router=admin.router,
    prefix='/admin',
    dependencies=[Depends(jwt.verify)]
)

# Register socketio namespaces
io.register_namespace(ChatNamespace())
io.register_namespace(SupportNamespace(namespace='/support'))