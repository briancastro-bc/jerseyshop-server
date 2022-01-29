from typing import Dict, Any

from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
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
engine = create_engine(settings.DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@as_declarative(metadata=metadata)
class Base:

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()