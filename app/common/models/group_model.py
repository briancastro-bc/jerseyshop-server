from fastapi_utils.api_model import APIModel

from .permission_model import PermissionModel

class GroupBase(APIModel):
    code_name: str

class GroupCreate(GroupBase):
    name: str

class GroupModel(GroupCreate):
    id: int
    permissions: list[PermissionModel]