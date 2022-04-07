from abc import ABC, abstractproperty
from typing import Dict, Optional, Any

from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response, JSONResponse
from starlette.status import *

class HttpResponse(ABC):
    
    isHttpResponse: bool = True
    
    @property
    @abstractproperty
    def code(self) -> Optional[int]:
        return None
    
    @property
    @abstractproperty
    def message(self) -> Optional[str]:
        return None
    
    def __init__(self, body: Dict[str, Any], **kwargs) -> None:
        self.body = body
    
    def response(self) -> Optional[Response]:
        compatible_json = jsonable_encoder(self.body)
        response: JSONResponse = JSONResponse(compatible_json, self.code, media_type='application/json')
        return response

def isHttpResponse(obj: any) -> HttpResponse:
    return obj is isinstance(HttpResponse or type(obj) and obj != None and obj.isHttpResponse == True)

"""
    2xx HTTP RESPONSES SUCCESS
"""

class HttpResponseSucess(HttpResponse):
    
    isHttpResponseSuccess = True
    
    def __init__(self, body: Dict[str, any]=None) -> None:
        super().__init__(body)

def isHttpResponseSuccess(obj: any) -> HttpResponseSucess:
    return obj is isinstance(HttpResponseSucess or type(obj) and obj != None and obj.isHttpResponseSuccess == True)

class HttpResponseOK(HttpResponseSucess):
    
    isHttpResponseOK = True
    
    @property
    def code(self) -> int:
        return HTTP_200_OK
    
    @property
    def message(self) -> str:
        return "OK"
    
    def __init__(self, body: Dict[str, any]) -> None:
        super().__init__(body)

def isHttpResponseOK(obj: any) -> HttpResponseOK:
    return obj is isinstance(HttpResponseOK or type(obj) and obj != None and obj.isHttpResponseOK == True)

class HttpResponseCreated(HttpResponseSucess):
    
    isHttpResponseCreated = True
    
    @property
    def code(self) -> int:
        return HTTP_201_CREATED
    
    @property
    def message(self) -> str:
        return "CREATED"
    
    def __init__(self, body: Dict[str, any]) -> None:
        super().__init__(body)

def isHttpResponseCreated(obj: any) -> HttpResponseCreated:
    return obj is isinstance(HttpResponseCreated or type(obj) and obj != None and obj.isHttpResponseCreated == True)

class HttpResponseAccepted(HttpResponseSucess):
    
    isHttpResponseAccepted = True
    
    @property
    def code(self) -> int:
        return HTTP_202_ACCEPTED
    
    @property
    def message(self) -> str:
        return "ACCEPTED"
    
    def __init__(self, body: Dict[str, any]) -> None:
        super().__init__(body)

def isHttpResponseAccepted(obj: any) -> HttpResponseAccepted:
    return obj is isinstance(HttpResponseAccepted or type(obj) and obj != None and obj.isHttpResponseAccepted == True)

class HttpResponseNotContent(HttpResponseSucess):
    
    isHttpResponseNotContent = True
    
    @property
    def code(self) -> int:
        return HTTP_204_NO_CONTENT
    
    @property
    def message(self) -> str:
        return "CREATED"
    
    def __init__(self) -> None:
        super().__init__()
    
    def __call__(self) -> Any:
        return 

def isHttpResponseNotContent(obj: any) -> HttpResponseNotContent:
    return obj is isinstance(HttpResponseNotContent or type(obj) and obj != None and obj.isHttpResponseNotContent == True)

"""
    3xx HTTP RESPONSES REDIRECTION
"""

class HttpResponseRedirection(HttpResponse):
    
    isHttpResponseRedirection = True
    
    def __init__(self, body: Dict[str, any]) -> None:
        super().__init__(body)

def isHttpResponseRedirection(obj: any) -> HttpResponseRedirection:
    return obj is isinstance(HttpResponseRedirection or type(obj) and obj != None and obj.isHttpResponseRedirection == True)

class HttpResponseMovedPermanently(HttpResponseRedirection):
    
    isHttpResponseMovedPermanently = True
    
    @property
    def code(self) -> int:
        return HTTP_301_MOVED_PERMANENTLY
    
    @property
    def message(self) -> str:
        return "MOVED PERMANENTLY"
    
    def __init__(self, path: str) -> None:
        super().__init__()

def isHttpResponseMovedPermanently(obj: any) -> HttpResponseMovedPermanently:
    return obj is isinstance(HttpResponseMovedPermanently or type(obj) and obj != None and obj.isHttpMovedPermanently == True)

class HttpResponseFound(HttpResponseRedirection):
    
    isHttpResponseFound = True
    
    @property
    def code(self) -> int:
        return HTTP_302_FOUND
    
    @property
    def message(self) -> str:
        return "FOUND"
    
    def __init__(self, path: str, body: Dict[str, any]) -> None:
        super().__init__(body)

def isHttpResponseFound(obj: any) -> HttpResponseFound:
    return obj is isinstance(HttpResponseFound or type(obj) and obj != None and obj.isHttpResponseFound == True)

"""
    4xx HTTP RESPONSES CLIENT ERRORS.
"""

class HttpResponseClientError(HttpResponse):
    
    isHttpResponseClientError = True
    
    def __init__(self, body: Dict[str, any]) -> None:
        super().__init__(body)

def isHttpResponseClientError(obj: any) -> HttpResponseClientError:
    return obj is isinstance(HttpResponseClientError or type(obj) and obj != None and obj.isHttpResponseClientError == True)

class HttpResponseBadRequest(HttpResponseClientError):
    
    isHttpResponseBadRequest = True
    
    @property
    def code(self) -> int:
        return HTTP_400_BAD_REQUEST
    
    @property
    def message(self) -> str:
        return "BAD REQUEST"
    
    def __init__(self, body: Dict[str, any]) -> None:
        super().__init__(body)

def isHttpResponseBadRequest(obj: any) -> HttpResponseBadRequest:
    return obj is isinstance(HttpResponseBadRequest or type(obj) and obj != None and obj.isHttpResponseBadRequest == True)

class HttpResponseUnauthorized(HttpResponseClientError):
    
    isHttpResponseUnauthorized = True
    
    @property
    def code(self) -> int:
        return HTTP_401_UNAUTHORIZED
    
    @property
    def message(self) -> str:
        return "UNAUTHORIZED"
    
    def __init__(self, body: Dict[str, any]) -> None:
        super().__init__(body)

def isHttpResponseUnauthorized(obj: any) -> HttpResponseUnauthorized:
    return obj is isinstance(HttpResponseUnauthorized or type(obj) and obj != None and obj.isHttpResponseUnauthorized == True)

class HttpResponseForbidden(HttpResponseClientError):
    
    isHttpResponseForbidden = True
    
    @property
    def code(self) -> int:
        return HTTP_403_FORBIDDEN
    
    @property
    def message(self) -> str:
        return "FORBIDDEN"
    
    def __init__(self, body: Dict[str, any]) -> None:
        super().__init__(body)

def isHttpResponseForbidden(obj: any) -> HttpResponseForbidden:
    return obj is isinstance(HttpResponseForbidden or type(obj) and obj != None and obj.isHttpResponseForbidden == True)

class HttpResponseNotFound(HttpResponseClientError):
    
    isHttpResponseNotFound = True
    
    @property
    def code(self) -> int:
        return HTTP_404_NOT_FOUND
    
    @property
    def message(self) -> int:
        return "NOT FOUND"
    
    def __init__(self, body: Dict[str, any]) -> None:
        super().__init__(body)

def isHttpResponseNotFound(obj: any) -> HttpResponseNotFound:
    return obj is isinstance(HttpResponseNotFound or type(obj) and obj != None and obj.isHttpResponseNotFound == True)

class HttpResponseMethodNotAllowed(HttpResponseClientError):
    
    isHttpResponseMethodNotAllowed = True
    
    @property
    def code(self) -> int:
        return HTTP_405_METHOD_NOT_ALLOWED
    
    @property
    def message(self) -> str:
        return "METHOD NOT ALLOWED"
    
    def __init__(self, body: Dict[str, any]) -> None:
        super().__init__(body)

def isHttpResponseMethodNotAllowed(obj: any) -> HttpResponseMethodNotAllowed:
    return obj is isinstance(HttpResponseMethodNotAllowed or type(obj) and obj != None and obj.isHttpResponseMethodNotAllowed == True)

class HttpResponseNotAcceptable(HttpResponseClientError):
    
    isHttpResponseNotAcceptable = True
    
    @property
    def code(self) -> int:
        return HTTP_406_NOT_ACCEPTABLE
    
    @property
    def message(self) -> str:
        return "NOT ACCEPTABLE"
    
    def __init__(self, body: Dict[str, any]) -> None:
        super().__init__(body)

def isHttpResponseNotAcceptable(obj: any) -> HttpResponseNotAcceptable:
    return obj is isinstance(HttpResponseNotAcceptable or type(obj) and obj != None and obj.isHttpResponseNotAcceptable == True)

class HttpResponseRequestTimeout(HttpResponseClientError):
    
    isHttpResponseRequestTimeout = True
    
    @property
    def code(self) -> int:
        return HTTP_408_REQUEST_TIMEOUT
    
    @property
    def message(self) -> str:
        return "REQUEST TIMEOUT"
    
    def __init__(self, body: Dict[str, any]) -> None:
        super().__init__(body)

def isHttpResponseRequestTimeout(obj: any) -> HttpResponseRequestTimeout:
    return obj is isinstance(HttpResponseRequestTimeout or type(obj) and obj != None and obj.isHttpResponseRequestTimeout == True)

class HttpResponseConflict(HttpResponseClientError):
    
    isHttpResponseConflict = True
    
    @property
    def code(self) -> int:
        return HTTP_409_CONFLICT
    
    @property
    def message(self) -> str:
        return "CONFLICT"
    
    def __init__(self, body: Dict[str, any]) -> None:
        super().__init__(body)

def isHttpResponseConflict(obj: any) -> HttpResponseConflict:
    return obj is isinstance(HttpResponseConflict or type(obj) and obj != None and obj.isHttpResponseConflict == True)

class HttpResponseTooManyRequest(HttpResponseClientError):
    
    isHttpResponseTooManyRequest = True
    
    @property
    def code(self) -> int:
        return HTTP_429_TOO_MANY_REQUESTS
    
    @property
    def message(self) -> str:
        return "TOO MANY REQUEST"
    
    def __init__(self, body: Dict[str, any]) -> None:
        super().__init__(body)

def isHttpResponseTooManyRequest(obj: any) -> HttpResponseTooManyRequest:
    return obj is isinstance(HttpResponseTooManyRequest or type(obj) and obj != None and obj.isHttpResponseTooManyRequest == True)

"""
    5xx HTTP RESPONSES SERVER ERRORS
"""

class HttpResponseServerError(HttpResponse):
    
    isHttpResponseServerError = True
    
    def __init__(self, body: Dict[str, any], **kwargs) -> None:
        super().__init__(body, **kwargs)

def isHttpResponseServerError(obj: any) -> HttpResponseServerError:
    return obj is isinstance(HttpResponseServerError or type(obj) and obj != None and obj.isHttpResponseServerError == True)

class HttpResponseInternalServerError(HttpResponseServerError):
    
    isHttpResponseInternalServerError = True
    
    @property
    def code(self) -> int:
        return HTTP_500_INTERNAL_SERVER_ERROR
    
    @property
    def message(self) -> str:
        return "INTERNAL SERVER ERROR"
    
    @property
    def error(self) -> str:
        return None
    
    def __init__(self, body: Dict[str, any], **kwargs) -> None:
        super().__init__(body, **kwargs)
        self.error = kwargs['error']

def isHttpResponseInternalServerError(obj: any) -> HttpResponseInternalServerError:
    return obj is isinstance(HttpResponseInternalServerError or type(obj) and obj != None and obj.isHttpResponseInternalServerError == True)

class HttpResponseNotImplemented(HttpResponseServerError):
    
    isHttpResponseNotImplemented = True
    
    @property
    def code(self) -> int:
        return HTTP_501_NOT_IMPLEMENTED
    
    @property
    def message(self) -> str:
        return "NOT IMPLEMENTED"
    
    def __init__(self, body: Dict[str, any], **kwargs) -> None:
        super().__init__(body, **kwargs)

def isHttpResponseNotImplemented(obj: any) -> HttpResponseNotImplemented:
    return obj is isinstance(HttpResponseNotImplemented or type(obj) and obj != None and obj.isHttpResponseNotImplemented == True)