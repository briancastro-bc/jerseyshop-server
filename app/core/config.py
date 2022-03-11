from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, validator

"""
    :class Settings - Define las configuraciones base cargadas en variables de entorno para el uso
                    las mismas
"""
class Settings(BaseSettings):
    # Project environment variables.
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl]
    SECRET_KEY: str

    # Database environment variables.
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: str
    MYSQL_DATABASE: str
    MYSQL_DATABASE_URI: Optional[str] = None
    
    # SMTP environment variables.
    SMTP_HOSTNAME: str
    SMTP_TLS_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    
    # GOOGLE CREDENTIALS
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    @validator("MYSQL_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return f"mysql+aiomysql://{values.get('MYSQL_USER')}:{values.get('MYSQL_PASSWORD')}@{values.get('MYSQL_HOST')}:" \
               f"{values.get('MYSQL_PORT')}/{values.get('MYSQL_DATABASE')}"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
