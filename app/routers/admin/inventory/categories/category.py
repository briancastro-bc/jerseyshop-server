from fastapi import Depends
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import Category
from app.core.http import HttpResponseBadRequest, HttpResponseCreated, HttpResponseNotContent, HttpResponseNotFound, HttpResponseOK
from app.core.dependency import get_session
from app.common.models import CategoryModel, CategoryCreate, CategoryParcialUpdate

from .category_service import CategoryService

router = InferringRouter()

@cbv(router)
class CategoryController:
    
    def __init__(self) -> None:
        self.service = CategoryService()
    
    @router.get('/', response_model=CategoryModel, status_code=200)
    async def get_all(self, db: AsyncSession=Depends(get_session)):
        categories: Category = await self.service.get_all(db)
        if categories:
            return HttpResponseOK({
                "status": "success",
                "data": {
                    "categories": categories
                }
            }).response()
        return HttpResponseNotFound({
            "status": "fail",
            "data": {
                "message": "No hay categorias creadas"
            }
        }).response()
    
    @router.get('/{code}', response_model=CategoryModel, status_code=200)
    async def get_by_code(self, code: str, db: AsyncSession=Depends(get_session)):
        category: Category = await self.service.get_by_code(code, db)
        if category:
            return HttpResponseOK({
                "status": "success",
                "data": {
                    "category": category
                }
            }).response()
        return HttpResponseNotFound({
            "status": "fail",
            "data": {
                "message": "No se encontro la categoria"
            }
        }).response()
    
    @router.post('/create', response_model=CategoryCreate, status_code=201)
    async def create(self, category: CategoryCreate, db: AsyncSession=Depends(get_session)):
        category: Category = await self.service.create(category, db)
        if category:
            return HttpResponseCreated({
                "status": "success",
                "data": {
                    "message": "La categoria ha sido creada"
                }
            }).response()
        return HttpResponseBadRequest({
            "status": "fail",
            "data": {
                "message": "La catagoria ya existe"
            }
        }).response()
    
    @router.put('/update/{code}', response_model=None, status_code=201)
    async def update(self, code: str):
        pass
    
    @router.patch('/edit/{code}', response_model=CategoryModel, status_code=201)
    async def edit(self, code: str, category: CategoryParcialUpdate, db: AsyncSession=Depends(get_session)):
        category_updated: Category = await self.service.edit(code, category, db)
        if category_updated:
            return HttpResponseOK({
                "status": "success",
                "data": {
                    "message": "Se editaron los campos de la categoría correctamente",
                }
            }).response()
        return HttpResponseNotFound({
            "status": "fail",
            "data": {
                "message": "No se encontro la categoria que se quiere editar"
            }
        }).response()
    
    @router.delete('/delete/{code}', response_model=None, status_code=204)
    async def delete(self, code: str, db: AsyncSession=Depends(get_session)):
        deleted = await self.service.delete(code, db)
        if deleted:
            return HttpResponseNotContent().__call__()
        return HttpResponseNotFound({
            "status": "fail",
            "data": {
                "message": "No se encontro la categoria"
            }
        }).response()