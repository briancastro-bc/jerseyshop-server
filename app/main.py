from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database import metadata, engine, database

from app.routers import auth

def create_application():
    
    # Create all tables in the database.
    metadata.create_all(bind=engine)
    
    _app = FastAPI(
        debug=True,
        title=settings.PROJECT_NAME,
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return _app

app = create_application()

@app.on_event('startup')
async def startup():
    await database.connect()
    
@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

app.include_router(auth.router, prefix='/auth')
