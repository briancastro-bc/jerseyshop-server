from typing import Optional 
from fastapi_utils.api_model import APIModel

from app.common.models import UserModel

import datetime

class RoomBase(APIModel):
    code: Optional[str]
    name: str
    
    class Config:
        arbitrary_types_allowed=True

class RoomCreate(RoomBase):
    limit: Optional[int]

class RoomModel(RoomCreate):
    owner: UserModel
    created_at: datetime.datetime
    is_active: Optional[bool]
    #users: Optional[List[User]]

class RoomUpdatePartial(APIModel):
    code: Optional[str]
    name: Optional[str]
    limit: Optional[int]
    is_active: Optional[bool]