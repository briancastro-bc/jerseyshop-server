from functools import wraps

from fastapi import Header, Response

from app.core.http import HttpResponseUnauthorized
from app.common.services import JwtService

import time, datetime

def refresh(Authorization: str=Header(None)):
    def _refresh_token(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            current_token: str = Authorization.split(' ')[1]
            decoded = JwtService.decode(encoded=current_token, validate=True)
            # Token expired
            if type(decoded) is dict:
                return HttpResponseUnauthorized({
                    "status": "fail",
                    "data": {
                        decoded
                    }
                })
            # Token is expire soon. It going to refresh
            if decoded['exp'] >= time.time() + 600:
                new_token: str = JwtService.encode(
                    payload={
                        "iss": "jerseyshop.com",
                        "sub": decoded['sub'],
                        "iat": datetime.datetime.utcnow(),
                        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
                    },
                    encrypt=True
                )
                response = Response()
                response.headers['Authorization'] = 'Bearer {0}'.format(new_token)
                # Return the new token.
                return new_token
            # The token isn't expired
            return f(*args, **kwargs)
        return wrapper
    return _refresh_token