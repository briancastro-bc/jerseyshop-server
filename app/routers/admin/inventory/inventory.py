
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

from .categories import category
from .products import product

router = InferringRouter()

router.include_router(
    router=category.router,
    prefix='/category'
)

router.include_router(
    router=product.router,
    prefix='/product'
)

@cbv(router)
class InventoryController:
    
    def __init__(self) -> None:
        pass
    
    @router.get('/', response_model=None, status_code=200)
    async def root(self):
        return "Inventory controller works"