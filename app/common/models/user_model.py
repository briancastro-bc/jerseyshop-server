from typing import Optional, List

from pydantic import BaseModel, validator
from fastapi import HTTPException
from fastapi_utils.api_model import APIModel

from .permission_model import PermissionModel
from .group_model import GroupModel
from .product_model import ProductModel

import datetime

class UserBase(APIModel):
    email: str
    password: str
    
    @validator('email', pre=True, always=True)
    def email_contain_at_and_dot(cls, v: str):
        if '@' not in v:
            raise HTTPException(status_code=400, detail="Dirección de correo electrónico inválida")
        elif '.' not in v:
            raise HTTPException(status_code=400, detail='Dirección de correo electrónico inválida')
        return v
    
    @validator('password', pre=True, always=True)
    def password_minimun_size(cls, v: str):
        count = len(v)
        if count < 8:
            raise HTTPException(status_code=400, detail="La contraseña debe tener mínimo 8 caracteres")
        return v
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class UserCreate(UserBase):
    name: str
    last_name: str
    birthday: datetime.datetime
    accept_advertising: Optional[bool]
    accept_terms: Optional[bool]
    
    class Config:
        orm_mode = True
    
class UserModel(UserCreate):
    id: str
    is_verify: bool
    created_at: datetime.datetime
    #profile: Optional[Profile] # TODO: Add the profile field to the model
    groups: List[GroupModel]
    permissions: List[PermissionModel]
    favorites: List[ProductModel]
    
    class Config:
        orm_mode = True

class UserRecovery(BaseModel):
    email: str
    
    class Config:
        orm_mode = True

class RefreshToken(APIModel):
    access_token: str
    refresh_token: Optional[bool]

class UserResponseModel(APIModel):
    uid: str
    email: str
    name: str
    last_name: str
    birthday: datetime.datetime
    accept_advertising: Optional[bool]
    accept_terms: Optional[bool]
    is_verify: bool
    created_at: datetime.datetime
    #profile: Optional[Profile] # TODO: Add the profile field to the model
    groups: List[GroupModel]
    permissions: List[PermissionModel]
    favorites: List[ProductModel]