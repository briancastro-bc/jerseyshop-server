from fastapi import Depends
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy import select
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import Product, User
from app.core.http import HttpResponseBadRequest, HttpResponseCreated
from app.core.dependency import get_session
from app.common.models import ProductCreate

from .product_service import ProductService

router = InferringRouter()

@cbv(router)
class ProductController:
    
    def __init__(self) -> None:
        self.service = ProductService()
    
    @router.get('/', response_model=None, status_code=200)
    async def get_all(self):
        pass
    
    @router.get('/{code}', response_model=None, status_code=200)
    async def get_by_code(self, code: str):
        pass
    
    @router.post('/create', response_model=None, status_code=201)
    async def create(self, product: ProductCreate, db: AsyncSession=Depends(get_session)):
        product: Product = await self.service.create(product, db)
        if product:
            """query = await db.execute(select(User).where(User.accept_advertising == True))
            users_advertising = query.fetchall()
            print(users_advertising)"""
            return HttpResponseCreated({
                "status": "success",
                "data": {
                    "message": "Se ha creado el producto"
                }
            }).response()
        return HttpResponseBadRequest({
            "status": "fail",
            "data": {
                "message": "No pudimos crear el producto, reintente"
            }
        }).response()
            
    
    @router.put('/update/{code}', response_model=None, status_code=201)
    async def update(self, code: str):
        pass
    
    @router.patch('/edit/{code}', response_model=None, status_code=201)
    async def edit(self, code: str):
        pass
    
    @router.delete('/delete/{code}', response_model=None, status_code=204)
    async def delete(self, code: str):
        pass