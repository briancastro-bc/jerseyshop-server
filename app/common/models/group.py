from typing import List

from fastapi_utils.api_model import APIModel

from .permission import Permission

class GroupBase(APIModel):
    name: str
    code_name: str

class GroupCreate(GroupBase):
    pass

class Group(GroupCreate):
    id: int
    permissions: List[Permission]
    
    class Config:
        orm_mode = True