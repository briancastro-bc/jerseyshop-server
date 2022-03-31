from app import namespaces
from app.core import settings

import socketio

def create_io_server() -> socketio.AsyncServer:
    sio = socketio.AsyncServer(
        logger=True,
        async_mode='asgi',
        ping_interval=30000,
        ping_timeout=100000,
        always_connect=True,
        cookie='io_session',
        cors_allowed_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        cors_credentials=True,
    )
    
    sio.register_namespace(namespaces.SupportNamespace(namespace='/support'))
    
    return sio