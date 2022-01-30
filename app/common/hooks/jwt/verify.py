from typing import Optional
from functools import wraps

from fastapi import Header, Depends
from sqlalchemy.orm import Session

from app.core.http import HttpResponseUnauthorized
from app.core.schemas import User
from app.common.services import JwtService
from app.database import get_db

def verify(authorization: str=Header(None), db: Session=Depends(get_db), validate_account: Optional[bool]=False):
    def _verify_token(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token: str = authorization.split(' ')[1]
            decoded = JwtService.decode(encoded=token, validate=True)
            if type(decoded) is dict:
                return HttpResponseUnauthorized({
                    "stauts": "fail",
                    "data": {
                        decoded
                    }
                }).response()
            if validate_account:
                db_user = db.query(User).filter_by(uid=decoded['sub']).first()
                if db_user.is_verify:
                    return f(*args, **kwargs)
                return HttpResponseUnauthorized({
                    "status": "fail",
                    "data": {
                        "message": "Verifica tu cuenta para poder acceder"
                    }
                }).response()
            return f(*args, **kwargs)
        return wrapper
    return _verify_token
        