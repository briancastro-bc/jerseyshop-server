import socketio
from fastapi import Depends

from .core import init, database
from .app import create_application
from .io import create_io_server
from .modules import auth, admin, account, root
from .common.hooks import jwt, required

app = create_application()
sio = create_io_server()

app.include_router(
    router=root.router,
    tags=['Root']
)
app.include_router(
    router=auth.router, 
    prefix='/auth',
    tags=['Authentication']
)
app.include_router(
    router=account.router,
    prefix='/account',
    dependencies=[
        Depends(jwt.verify(validate_account=False)),
        Depends(required.group(['users']))
    ],
    tags=['Account']
)
app.include_router(
    router=admin.router,
    prefix='/admin',
    dependencies=[
        Depends(jwt.verify(validate_account=True)),
        Depends(required.group(['users']))
    ],
    tags=['Administration']
)

@app.on_event('startup')
async def on_startup():
    print("Start up application")
    await init()
    await database.connect()
    
@app.on_event('shutdown')
async def on_shutdown():
    print("Shutting down application")
    await database.disconnect()

io_app = socketio.ASGIApp(
    sio, 
    app
)