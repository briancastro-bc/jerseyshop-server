from fastapi import Depends

from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

from . import dashboard, advertisement, inventory

router = InferringRouter()

router.include_router(
    router=dashboard.router,
    prefix='/dashboard',
)
router.include_router(
    router=advertisement.router,
    prefix='/advertisements'
)
router.include_router(
    router=inventory.router,
    prefix='/inventory'
)

@cbv(router)
class AdminController:
    
    def __init__(self) -> None:
        pass
    
    @router.get('/', response_model=None, status_code=200)
    async def panel(self):
        return "admin panel works"
