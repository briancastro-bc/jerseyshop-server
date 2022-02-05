from typing import List

from fastapi import Depends, HTTPException

from app.core.schemas import User
from app.core.dependency import get_current_user

def permission(code_name: List[str]):
    def _permission(current_user: User=Depends(get_current_user)):
        for permission in code_name:
            if permission in current_user.permissions:
                return
        raise HTTPException(
            403,
            {
                "status": "fail",
                "data": {
                    "message": "El usuario no tiene los permisos requeridos"
                }
            }
        )
    return _permission
