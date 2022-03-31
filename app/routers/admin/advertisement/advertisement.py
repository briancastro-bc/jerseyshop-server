from typing import Optional
from fastapi import Depends, Query, Path, BackgroundTasks
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import Advertisement
from app.core.http import HttpResponseBadRequest, HttpResponseCreated, HttpResponseNotContent, HttpResponseNotFound, HttpResponseOK
from app.core.dependency import get_session, Dependency
from app.common.models import AdvertisementCreate, AdvertisementModel, AdvertisementPartialUpdate
from app.common.services import EmailService
from app.common.helpers import NOTIFY_FORMAT

from .advertisement_service import AdvertisementService

router = InferringRouter()

@cbv(router)
class AdvertisementController:
    
    def __init__(self) -> None:
        self.email = EmailService()
    
    @router.get('/', response_model=AdvertisementModel, status_code=200)
    async def get_all(
        self, 
        order_by: Optional[int]=Query(
            2,
            title='Orden',
            description='Ordenar anuncios por ...'
        ),
        limit: Optional[int]=Query(
            100, 
            title='Limite', 
            description="Limite de anuncios que se deben mostrar"
        ),
        skip: Optional[int]=Query(
            0,
            title='Salto',
            description='Salto inicial de los anuncios creados'
        ),
        session: AsyncSession=Depends(Dependency.get_session)
    ):
        advertisements: list[Advertisement] = await AdvertisementService.get_all_protected(
            order_by=order_by,
            limit=limit,
            skip=skip,
            session=session
        )
        if advertisements:
            return HttpResponseOK({
                "status": "success",
                "data": {
                    "advertisements": advertisements
                }
            }).response()
        return HttpResponseNotFound({
            "status": "fail",
            "data": {
                "message": "No se encontraron anuncios"
            }
        }).response()
        
    @router.get('/{uid}', response_model=AdvertisementModel, status_code=200)
    async def get_by_id(
        self, 
        uid: str=Path(
            ...,
            title='UID',
            description='ID del anuncio el cual se quiere buscar'
        ),
        session=Depends(Dependency.get_session)
    ):
        advertisement: Advertisement = await AdvertisementService.get_one_protected(
            uid=uid,
            session=session
        )
        if advertisement:
            return HttpResponseOK({
                "status": "success",
                "data": {
                    "advertisement": advertisement
                }
            }).response()
        return HttpResponseNotFound({
            "status": "fail",
            "data": {
                "message": "No se encontro el anuncio"
            }
        }).response()
    
    @router.post('/', response_model=AdvertisementCreate, status_code=201)
    async def create(
        self, 
        advertisement: AdvertisementCreate,
        backgroundTasks: BackgroundTasks,
        session: AsyncSession=Depends(Dependency.get_session),
    ):
        new_advertisement: Advertisement = await AdvertisementService.create_one(
            advertisement=advertisement,
            session=session
        )
        if new_advertisement:
            if advertisement.notify:
                result = await session.execute(
                    text('SELECT email FROM users WHERE accept_advertising = true')
                )
                users: list = result.all()
                emails = [user['email'] for user in users]
                backgroundTasks.add_task(
                    self.email.send_email,
                    emails,
                    'Tenemos noticias para ti',
                    message=NOTIFY_FORMAT.format(new_advertisement.description, new_advertisement.hyperlink),
                    format='html'
                )
            return HttpResponseCreated({
                "status": "success",
                "data": {
                    "message": "Se ha creado el anuncio satisfactoriamente"
                }
            }).response()
        return HttpResponseBadRequest({
            "status": "fail",
            "data": {
                "message": "No hemos podido crear el anuncio"
            }
        }).response()
    
    @router.put('/{uid}', response_model=AdvertisementModel, status_code=201)
    async def update(
        self, 
        advertisement: AdvertisementModel,
        uid: str=Path(
            ...,
            title='Actualizar',
            description='Actualizar un anuncio en su totalidad'
        ),
        session=Depends(Dependency.get_session)
    ):
        updated_advertisement: Advertisement = await AdvertisementService.update_one(
            advertisement=advertisement,
            uid=uid,
            session=session
        )
        if updated_advertisement:
            return HttpResponseCreated({
                "status": "success",
                "data": {
                    "message": "Se ha actualizado el anuncio"
                }
            }).response()
        return HttpResponseBadRequest({
            "status": "fail",
            "data": {
                "message": "No pudimos actualizar el anuncio"
            }
        }).response()
    
    @router.patch('/{uid}', response_model=AdvertisementModel, status_code=201)
    async def edit(
        self,
        advertisement: AdvertisementPartialUpdate,
        uid: str=Path(
            ...,
            title='Editar',
            description='Determina la edicion parcial de un anuncio'
        ),
        session=Depends(Dependency.get_session)
    ):
        edited_advertisement: Advertisement = await AdvertisementService.edit_one(
            advertisement=advertisement,
            uid=uid,
            session=session
        )
        if edited_advertisement:
            return HttpResponseCreated({
                "status": "success",
                "data": {
                    "message": "Se ha editado el anuncio"
                }
            }).response()
        return HttpResponseBadRequest({
            "status": "fail",
            "data": {
                "message": "No se pudo editar el anuncio"
            }
        }).response()
    
    @router.delete('/{uid}', response_model=None, status_code=200)
    async def delete(
        self, 
        uid: str=Path(
            ...,
            title='Eliminar',
            description='Determina la elminicacion de un anuncio especifico'
        ), 
        session: AsyncSession=Depends(get_session)
    ):
        was_deleted = await AdvertisementService.delete_one(
            uid=uid,
            session=session
        )
        if was_deleted:
            return HttpResponseOK({
                "status": "success",
                "data": {
                    "message": "El anuncio ha sido eliminado"
                }
            }).response()
        return HttpResponseBadRequest({
            "status": "fail",
            "data": {
                "message": "No pudimos eliminar el anuncio"
            }
        }).response()
        