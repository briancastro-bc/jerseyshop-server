from typing import Dict, Any

from databases import Database
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from app.core.config import settings

conventions: Dict[str, Any] = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s" 
}

# Define asynchronous database.
database = Database(settings.DATABASE_URI)
metadata = MetaData(naming_convention=conventions)
engine = create_async_engine(settings.DATABASE_URI, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession, autocommit=False, autoflush=False)

@as_declarative(metadata=metadata)
class Base:

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

async def get_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
        