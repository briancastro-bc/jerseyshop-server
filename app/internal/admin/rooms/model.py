from typing import Optional, List

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