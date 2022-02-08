from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.init import init_models
from app.common.namespaces import ChatNamespace, SupportNamespace
from app.common.hooks import jwt, required
from app.database import database

from app.routers import auth, home
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
        expose_headers=["X-Refresh-Token"]
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

app.include_router(router=home.router)
app.include_router(router=auth.router, prefix='/auth')
app.include_router(
    router=admin.router,
    prefix='/admin',
    dependencies=[
        Depends(jwt.verify),
        #Depends(required.group(['users']))
    ]
)

# Register socketio namespaces
io.register_namespace(ChatNamespace())
io.register_namespace(SupportNamespace(namespace='/support'))