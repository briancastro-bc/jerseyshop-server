from fastapi_utils.api_model import APIModel

class PermissionBase(APIModel):
    code_name: str

class PermissionCreate(PermissionBase):
    name: str

class PermissionModel(PermissionCreate):
    id: int