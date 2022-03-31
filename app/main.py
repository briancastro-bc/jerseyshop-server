from app.core import init_models, database
from app.io import create_io_server

from .app import create_application

import socketio

app = create_application()
sio: socketio.AsyncServer = create_io_server()
io_app = socketio.ASGIApp(
    sio, 
    app
)

@app.on_event('startup')
async def startup():
    await init_models()
    await database.connect()
    
@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()