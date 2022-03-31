from fastapi import Depends
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

from . import dashboard, advertisement, inventory, room

router = InferringRouter()

router.include_router(
    router=dashboard.router,
    prefix='/dashboard',
    tags=['Dashboard']
)
router.include_router(
    router=advertisement.router,
    prefix='/advertisements',
    tags=['Advertisements']
)
router.include_router(
    router=inventory.router,
    prefix='/inventory',
    tags=['Inventory']
)
router.include_router(
    router=room.router,
    prefix='/rooms',
    tags=['Rooms']
)

@cbv(router)
class AdminController:
    
    def __init__(self) -> None:
        pass
    
    @router.get('/', response_model=None, status_code=200)
    async def panel(self):
        return "admin panel works"

    @router.get('/supportRooms', response_model=None, status_code=200)
    async def support_rooms(self):
        return "All support rooms created at moment"