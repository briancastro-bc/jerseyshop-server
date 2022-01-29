from typing import Optional, List
from pydantic import validator

from fastapi import HTTPException

from fastapi_utils.api_model import APIModel

from .permission import Permission
from .group import Group

import datetime

class UserBase(APIModel):
    email_address: str
    password: str
    
    @validator('email_address', pre=True, always=True)
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
    birthday: datetime.date
    accept_advertising: Optional[bool]
    accept_terms: Optional[bool]
    
    class Config:
        orm_mode = True
    
class UserModel(UserCreate):
    id: str
    is_verify: bool
    created_at: datetime.datetime
    groups: List[Group]
    permissions: List[Permission]
    
    class Config:
        orm_mode = True