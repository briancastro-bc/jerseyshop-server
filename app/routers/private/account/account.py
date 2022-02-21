from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

router = InferringRouter()

@cbv(router)
class AccountController:
    
    def __init__(self) -> None:
        pass
    
    @router.get('/', response_model=None, status_code=200)
    async def get(self):
        return "Account works"
    
    @router.get('/{uid}', response_model=None, status_code=200)
    async def get_by_id(self, uid: str):
        pass
    
    @router.put('/{uid}', response_model=None, status_code=201)
    async def update(self, uid: str):
        pass
    
    @router.patch('/{uid}', response_model=None, status_code=204)
    async def edit(self, uid: str):
        pass