from fastapi import Depends, HTTPException

from app.core.schemas import User
from app.core.dependency import get_user

def permission(code_name: list[str]):
    def _permission(
        current_user: User=Depends(get_user(
            current=True
        ))
    ):
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
