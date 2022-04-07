from fastapi import Depends, UploadFile, File
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.http_responses import HttpResponseNotFound
from app.core.dependency import get_session
from app.common.services import FileService, FileType

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
        self.file_service = FileService()
    
    @router.get('/', response_model=None, status_code=200)
    async def root(self):
        return "Inventory controller works"
    
    @router.post('/importInventory', response_model=None, status_code=201)
    async def import_inventory(
        self, 
        file: UploadFile=File(..., title='Excel file to import in the server for construct an inventory'),
        db: AsyncSession=Depends(get_session)
    ):
        if not file:
            return HttpResponseNotFound({
                "status": "fail",
                "data": {
                    "message": "No se envio un archivo de importación"
                }
            }).response()
        save = self.file_service.upload_file(file)
        imported = await self.file_service.import_excel_file(file, db)
        return imported
        