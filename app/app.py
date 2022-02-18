from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.core import settings
from app.routers import home, auth, admin
from app.common.hooks import jwt, required

"""
    :function create_application - Construye la instancia de FastAPI y configura todo
    lo relacionado con el servidor.
    :returns instancia de FastAPI.
"""
def create_application() -> FastAPI:
    
    _app = FastAPI(
        debug=True,
        title=settings.PROJECT_NAME,
        description="""
            Servidor de recursos de Jerysey Shop, abastece toda la información y módulos
            relacionados al sistema de la tienda virtual.
        """,
        version='0.9.1',
        contact=dict(email='yitocode@gmail.com', github='briancastro-bc')
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Refresh-Token"]
    )
    
    _app.include_router(router=home.router)
    _app.include_router(router=auth.router, prefix='/auth')
    _app.include_router(
        router=admin.router,
        prefix='/admin',
        dependencies=[
            Depends(jwt.verify(validate_account=True)),
            Depends(required.group(['users']))
        ]
    )
    
    return _app