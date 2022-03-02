from fastapi import Depends
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import User
from app.core.http import HttpResponseOK
from app.core.dependency import get_current_user, get_session
from app.common.models import UserResponseModel

from .account_service import AccountService

router = InferringRouter()

@cbv(router)
class AccountController:
    
    def __init__(self) -> None:
        self.account_service = AccountService()
    
    @router.get('/', response_model=UserResponseModel, status_code=200)
    async def my_account(self, current_user: User=Depends(get_current_user), db: AsyncSession=Depends(get_session)):
        user: User = await self.account_service.my_account(current_user, db)
        userResponse = UserResponseModel(**user.__dict__)
        if user:
            return HttpResponseOK({
                "status": "success",
                "data": {
                    "user": userResponse
                }
            }).response()
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