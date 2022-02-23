from typing import Optional, List
from unicodedata import name

from fastapi_utils.api_model import APIModel

from app.core.schemas import User

class RoomBase(APIModel):
    code: Optional[str]
    name: str

class RoomCreate(RoomBase):
    limit: Optional[int]

class RoomModel(RoomCreate):
    is_active: Optional[bool]
    #users: Optional[List[User]]

class RoomUpdatePartial(APIModel):
    code: Optional[str]
    name: Optional[str]
    limit: Optional[int]
    is_active: Optional[bool]