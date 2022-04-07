from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from .core import settings

"""
    :function create_application - Construye la instancia de FastAPI y configura todo
    lo relacionado con el servidor.
    :returns instancia de la aplicacion aplicando las configuraciones.
"""
def create_application() -> FastAPI:
    
    app = FastAPI(
        debug=True,
        title=settings.SERVER_NAME,
        description="""
            Servidor de recursos de Jerysey Shop, abastece toda la información y módulos
            relacionados al sistema de la tienda virtual.
        """,
        version='0.9.1',
        contact=dict(
            email='yitocode@gmail.com', 
            github='https://github.com/briancastro-bc'
        )
    )

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=[str(origin) for origin in settings.SERVER_CORS_ORIGINS],
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Refresh-Token"]
    )
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.SERVER_SECRET_KEY
    )
    
    
    return app