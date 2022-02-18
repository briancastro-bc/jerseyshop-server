
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

router = InferringRouter()

@cbv(router)
class InventoryController:
    
    def __init__(self) -> None:
        pass
    
    @router.get('/inventory', response_model=None, status_code=200)
    async def inventory(self):
        return "Inventory controller works"