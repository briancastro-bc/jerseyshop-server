from app.core import settings, init_models, database
from app.common.namespaces import SupportNamespace

from .app import create_application

import socketio

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

# Register socketio namespaces
io.register_namespace(SupportNamespace(namespace='/support'))