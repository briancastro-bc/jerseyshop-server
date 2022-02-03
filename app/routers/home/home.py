
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

from app.core.http import HttpResponseOK

router = InferringRouter()

@cbv(router)
class HomeController:
    
    def __init__(self) -> None:
        pass
    
    @router.get('/', response_model=None, status_code=201)
    async def create_room(self):
        return HttpResponseOK({
            "status": "success",
            "data": {
                "message": "Hello World!",
            }
        }).response()