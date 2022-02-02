from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.common.namespaces import ChatNamespace, SupportNamespace
from app.common.hooks import jwt
from app.database import database, init_models

from app.routers import auth
from app.internal import admin

import socketio

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

app.include_router(router=auth.router, prefix='/auth')
app.include_router(
    router=admin.router,
    prefix='/admin',
    dependencies=[Depends(jwt.verify)]
)

# Register socketio namespaces
io.register_namespace(ChatNamespace())
io.register_namespace(SupportNamespace(namespace='/support'))