from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.common.namespaces import ChatNamespace
from app.database import metadata, engine, database

from app.routers import auth

import socketio

def create_application():
    
    # Create all tables in the database.
    # metadata.drop_all(bind=engine)
    metadata.create_all(bind=engine)
    
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

io = socketio.AsyncServer(logger=True, cors_allowed_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS], async_mode='asgi', ping_timeout=30000)
app = create_application()
io_app = socketio.ASGIApp(io, app)

@app.on_event('startup')
async def startup():
    await database.connect()
    
@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

app.include_router(auth.router, prefix='/auth')

# Register socketio namespaces
io.register_namespace(ChatNamespace())
