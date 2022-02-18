
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

router = InferringRouter()

@cbv(router)
class DashboardController:
    
    def __init__(self) -> None:
        pass
    
    @router.get('/', response_model=None, status_code=200)
    async def dashboard(self):
        return "dashboard controller works!"