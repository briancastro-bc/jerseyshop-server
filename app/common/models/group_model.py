from typing import List

from fastapi_utils.api_model import APIModel

from .permission_model import PermissionModel

class GroupBase(APIModel):
    name: str
    code_name: str

class GroupCreate(GroupBase):
    pass

class GroupModel(GroupCreate):
    id: int
    permissions: List[PermissionModel]
    
    class Config:
        orm_mode = True