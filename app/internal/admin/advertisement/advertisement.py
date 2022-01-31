
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

router = InferringRouter()

@cbv(router)
class AdvertisementController:
    
    def __init__(self) -> None:
        pass
    
    @router.get('/', response_model=None, status_code=200)
    async def advertisement(self):
        return "advertisement controller works!"