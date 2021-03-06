from typing import Dict, Any, Optional
from authlib.jose import jwt, errors 
from authlib.common.encoding import to_bytes, to_unicode

from app.core.http_responses import HttpResponseInternalServerError

from .file import FileService, RSAKeyType

class JwtService:
    
    __headers__: Dict[str, Any] = {
        "alg": "RS256"
    }
    
    @classmethod
    def encode(cls, payload: Dict[str, Any], encrypt: Optional[bool] = None) -> Optional[str]:
        key: str = FileService.getRSAKey(RSAKeyType.PRIVATE.value)
        if key is None:
            return HttpResponseInternalServerError({
                "status": "error",
                "message": "No se ha provisto una llave privada",
                "code": 500
            }).response()
        if encrypt:
            cls.__headers__ = {
                "alg": "RSA-OAEP-256",
                "enc": "A256GCM"
            }
        encoded: bytes = jwt.encode(cls.__headers__, payload, key, check=True)
        token: str = to_unicode(encoded)
        return token
        
    @classmethod
    def decode(cls, encoded: str, validate: bool | None):
        key: str = FileService.getRSAKey(RSAKeyType.PRIVATE.value)
        encoded = to_bytes(encoded)
        dot_count = encoded.count(b'.')
        if key is None:
            return dict(message="No se ha provisto una llave firmada (RSA)")
        if dot_count == 2:
            key = FileService.getRSAKey(RSAKeyType.PUBLIC.value)
        try:
            payload = jwt.decode(encoded, key)
            if validate:
                import datetime
                payload.validate(leeway=datetime.timedelta(minutes=11).total_seconds())
        except errors.ExpiredTokenError:
            return dict(message="Token expirado")
        except errors.BadSignatureError:
            return dict(message="Token inválido")
        except errors.DecodeError:
            return dict(message="Error al decodificar el token")
        else:
            return payload