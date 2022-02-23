from fastapi import BackgroundTasks, Depends, Path
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import Product, User, Profile
from app.core.http import HttpResponseBadRequest, HttpResponseCreated, HttpResponseNotContent, HttpResponseNotFound, HttpResponseOK
from app.core.dependency import get_session
from app.common.services import EmailService
from app.common.models import ProductCreate, ProductModel, ProductPartialUpdate

from .product_service import ProductService

router = InferringRouter()

@cbv(router)
class ProductController:
    
    def __init__(self) -> None:
        self.service = ProductService()
        self.email = EmailService()
    
    @router.get('/', response_model=ProductModel, status_code=200)
    async def get_all(self, db: AsyncSession=Depends(get_session)):
        products: Product = await self.service.get_all(db)
        if products:
            return HttpResponseOK({
                "status": "success",
                "data": {
                    "products": products
                }
            }).response()
        return HttpResponseNotFound({
            "status": "fail",
            "data": {
                "message": "No se encontraron productos"
            }
        }).response()
    
    @router.get('/{code}', response_model=ProductModel, status_code=200)
    async def get_by_code(self, code: str=Path(None, title="Get by product code"), db: AsyncSession=Depends(get_session)):
        product: Product = await self.service.get_by_code(code, db)
        if product:
            return HttpResponseOK({
                "status": "success",
                "data": {
                    "product": product
                }
            }).response()
        return HttpResponseNotFound({
            "status": "fail",
            "data": {
                "message": "No se encontro el producto"
            }
        }).response()
    
    @router.post('/create', response_model=ProductCreate, status_code=201)
    async def create(self, product: ProductCreate, background_task: BackgroundTasks, db: AsyncSession=Depends(get_session)):
        product: Product = await self.service.create(product, db)
        if product:
            query = await db.execute(
                select(User.email)
                .where(User.accept_advertising == True)
            )
            users_advertising = query.unique().fetchall()
            emails = [email['email'] for email in users_advertising]
            message_format: str = """
                <center>
                    <div style="padding: 0%;
                    margin: 0%;
                    width: 75%;
                    height: 100%;
                    border:1px solid rgba(0,0,0,0.25);
                    padding: 24px;
                    border-radius: 25px;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;"
                    >
                    <img style="width: 75%;
                                float: left;
                                margin-left: 16%;"
                    src="https://i.imgur.com/ezOUjf5.png" alt="Company logo">
                    <br style="clear: both;">
                    <center>
                    <h1 style="font-weight: 400;">¡Nuevos productos para ti <strong>{0}</strong>! Ven a ver que hay de nuevo.</h1> <h2 style="font-weight: 400; font-size:24px;"><br>Podras disfrutar de nuevos estilos a tu gusto y demas</h2>
                    <h2 style="font-weight: 400;">Sólo falta un último paso, y, con esto, podrás acceder a las <strong>compras online</strong> y <strong>contenido único para tí</strong>
                    <br><br>
                    <a style="color: white;
                            padding: 10px;
                            background-color: rgb(10, 137, 255);
                            font-style: none;
                            text-decoration: none;
                            font-size: 1.3rem;"
                        href="http://localhost:8000/product/{1}">Ver contenido</a>
                    </h2>
                    </center>
                </div>
                </center>
            """.format(product.name, product.code)
            background_task.add_task(
                self.email.send_email,
                emails,
                "Nuevos productos para ti",
                message=message_format,
                format='html'
            )
            return HttpResponseCreated({
                "status": "success",
                "data": {
                    "message": "Se ha creado el producto",
                }
            }).response()
        return HttpResponseBadRequest({
            "status": "fail",
            "data": {
                "message": "No pudimos crear el producto, reintente"
            }
        }).response()
    
    @router.put('/update/{code}', response_model=ProductModel, status_code=201)
    async def update(self, product: ProductModel, code: str=Path(None, title="Update product by code")):
        pass
    
    @router.patch('/edit/{code}', response_model=ProductModel, status_code=201)
    async def edit(
        self, 
        product: ProductPartialUpdate, 
        code: str=Path(None, title="Edit product by code"), 
        db: AsyncSession=Depends(get_session)
    ):
        product_updated: Product = await self.service.edit(product, code, db)
        if product_updated:
            return HttpResponseCreated({
                "status": "success",
                "data": {
                    "message": "El producto fue editado correctamente"
                }
            }).response()
        return HttpResponseBadRequest({
            "status": "fail",
            "data": {
                "message": "No fue posible editar el producto"
            }
        }).response()
    
    @router.delete('/delete/{code}', response_model=None, status_code=204)
    async def delete(self, code: str=Path(None, title="Delete product by code"), db: AsyncSession=Depends(get_session)):
        is_deleted = await self.service.delete(code, db)
        if is_deleted:
            return HttpResponseNotContent().__call__()
        return HttpResponseBadRequest({
            "status": "fail",
            "data": {
                "message": "No se pudo borrar el producto"
            }
        }).response()