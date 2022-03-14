from fastapi import HTTPException
from sqlalchemy import text, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import Advertisement
from app.common.models import AdvertisementCreate, AdvertisementPartialUpdate, AdvertisementModel

class AdvertisementService:
    
    """
        :classmethod get_all_public - Retorna toda la informacion publica de los anuncios que ven los usuarios
    """
    @classmethod
    async def get_all_public(
        cls, 
        session: AsyncSession
    ):
        try:
            result = await session.execute(
                text('SELECT title, hyperlink, description, time_ago, expired_date FROM advertisements WHERE is_active = true ORDER BY time_ago ASC')
            )
            advertisements: list[Advertisement] = result.all()
            return advertisements
        except:
            raise HTTPException(
                400,
                {
                    "status": "fail",
                    "data": {
                        "message": "No fue posible mostrar los anuncios"
                    }
                }
            )
    
    """
        :classmethod get_all_protected - Retorna la informacion de todos los anuncios
        que pueden ver los adminitradores de la aplicacion
        :param order_by - Especifica a partir de cual metrica se ordenaran los anuncios
        :param limit - Especifica el limite de anuncios a mostrar
        :param skip - Especifica apartir de que anuncio comienza el limite
    """
    @classmethod
    async def get_all_protected(
        cls, 
        order_by: int, 
        limit: int, 
        skip: int, 
        session: AsyncSession
    ):
        try:
            result = await session.execute(
                text('SELECT * FROM advertisements ORDER BY :order_by ASC LIMIT :limit OFFSET :skip').\
                bindparams(
                    order_by=order_by,
                    limit=limit,
                    skip=skip
                )
            )
            advertisements: list[Advertisement] = result.all()
            return advertisements
        except Exception as e:
            raise HTTPException(
                400,
                {
                    "status": "fail",
                    "data": {
                        "message": "No pudimos mostrar los anuncios del sistema"
                    }
                }
            )

    """
        :classmethod get_one_protected - Retorna un anuncio especifico del administrador.
        :param uid - Especifica el uid del anuncio a mostrar.
    """
    @classmethod
    async def get_one_protected(
        cls, 
        uid: str, 
        session: AsyncSession
    ):
        try:
            result = await session.execute(
                text('SELECT * FROM advertisements WHERE uid=:uid').\
                bindparams(
                    uid=uid
                )
            )
            advertisement: Advertisement = result.first()
            return advertisement
        except Exception as e:
            raise HTTPException(
                400,
                {
                    "status": "fail",
                    "data": {
                        "message": "No pudimos mostrar el anuncio"
                    }
                }
            )
    
    """
        :classmethod create_one - Crea un nuevo anuncio en la base de datos.
        :param advertisement - Objeto que trae las caracteristicas y propiedades del nuevo anuncio
    """
    @classmethod
    async def create_one(
        cls, 
        advertisement: AdvertisementCreate, 
        session: AsyncSession
    ):
        try:
            new_advertisement = Advertisement(**advertisement.dict(
                exclude={'uid', 'notify'}
            ))
            session.add(new_advertisement)
            await session.commit()
            return new_advertisement
        except Exception as e:
            raise HTTPException(400, {
                "status": "fail",
                "data": {
                    "message": "Tuvimos un error, no pudimos crear el anuncio",
                    "exception": e
                }
            })
    
    """
        :classmethod update_one - Permite actualizar un anuncio completo
        :param advertisement - El objeto que se va a actualizar
        :param uid - El id de ese objeto especifico
    """
    @classmethod
    async def update_one(
        cls,
        advertisement: AdvertisementModel,
        uid: str,
        session: AsyncSession
    ):
        try:
            updated_advertisement = await session.execute(
                update(Advertisement).values(
                    **advertisement.dict()
                ).where(Advertisement.uid == uid)
            )
            await session.commit()
            return updated_advertisement
        except Exception as e:
            return None
    
    """
        :classmethod edit_one - Permite editar parcialmente un anuncio haciendo que se actualice unicamente un elemento.
        :param advertisement - El objeto parcial que se va a actualizar
        :param uid - El identificador de ese objeto.
    """
    @classmethod
    async def edit_one(
        cls,
        advertisement: AdvertisementPartialUpdate,
        uid: str,
        session: AsyncSession
    ):
        try:
            edited_advertisement = await session.execute(
                update(Advertisement).values(
                    **advertisement.dict(
                        exclude_unset=True
                    )
                ).where(Advertisement.uid == uid)
            )
            await session.commit()
            return edited_advertisement
        except Exception as e:
            return None
    
    """
        :classmethod delete_one - Permite borrar un anuncio especifico.
        :param uid - El identificador de ese anuncio especifico.
    """
    @classmethod
    async def delete_one(
        cls,
        uid: str,
        session: AsyncSession
    ):
        try:
            await session.execute(
                delete(Advertisement).where(Advertisement.uid == uid)
            )
            await session.commit()
            return True
        except Exception as e:
            return False