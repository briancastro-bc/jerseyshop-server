from typing import Optional, Any
from pydantic import Field, validator
from fastapi_utils.api_model import APIModel
import datetime

class AdvertisementBase(APIModel):
    uid: Optional[str]
    title: str = Field(
        ...,
        title='Titulo',
        description='Titulo representativo del anuncio a crear',
        max_length=40
    )
    description: str = Field(
        ...,
        title='Descripcion',
        description='Detalles de los anuncios creados',
        max_length=300
    )

class AdvertisementCreate(AdvertisementBase):
    notify: bool = Field(
        ...,
        title='Notificar',
        description='Especifica si el anuncio se notificara por correo electronico a los usuarios'
    )
    hyperlink: Optional[str] = Field(
        None,
        title='Hipervinculo',
        description='Determina el enlace externo del anuncio',
        max_length=150
    )
    is_public: Optional[bool] = Field(
        None,
        title='Visibilidad',
        description='Especifica la visibilidad del anuncio'
    )
    is_active: Optional[bool] = Field(
        None,
        title='Estado',
        description='Determina el estado del anuncio'
    )
    expired_date: datetime.datetime = Field(
        ...,
        title='Fecha limite',
        description='Especifica la fecha limite la cual durara el anuncio'
    )
    
    @validator('expired_date')
    def valid_expired_date(cls, v: Any):
        pass

class AdvertisementModel(AdvertisementCreate):
    time_ago: Optional[datetime.datetime]

class AdvertisementPartialUpdate(APIModel):
    title: Optional[str]
    description: Optional[str]
    hyperlink: Optional[str]
    is_active: Optional[bool]
    is_public: Optional[bool]
    expired_date: Optional[datetime.datetime]