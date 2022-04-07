from fastapi import Depends
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession

from .account_service import AccountService

from app.core import User
from app.core.http_responses import HttpResponseOK
from app.core.dependency import get_session, get_user
from app.common.models import UserResponseModel

router = InferringRouter()

@cbv(router)
class AccountController:
    
    def __init__(self) -> None:
        self.account_service = AccountService()
    
    @router.get('/', response_model=UserResponseModel, status_code=200)
    async def account(
        self, 
        current_user: User=Depends(get_user(
            current=True
        )), 
        session: AsyncSession=Depends(get_session)
    ):
        user: User = await AccountService.get_user_data(
            user=current_user,
            session=session
        )
        data = UserResponseModel(**user.__dict__)
        if user:
            return HttpResponseOK({
                "status": "success",
                "data": {
                    "user": data
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