from fastapi_utils.api_model import APIModel

class PermissionBase(APIModel):
    name: str
    code_name: str

class PermissionCreate(PermissionBase):
    pass

class PermissionModel(PermissionCreate):
    id: int
    
    class Config:
        orm_mode = True