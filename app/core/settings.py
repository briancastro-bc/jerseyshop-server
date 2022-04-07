from pydantic import AnyHttpUrl, BaseSettings, validator

"""
    :class Settings - Define las configuraciones base cargadas en variables de entorno para el uso
    las mismas
"""
class Settings(BaseSettings):
    SERVER_NAME: str
    SERVER_CORS_ORIGINS: list[AnyHttpUrl]
    SERVER_SECRET_KEY: str

    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: str
    MYSQL_DATABASE: str
    MYSQL_DATABASE_URI: str | None
    
    SMTP_HOSTNAME: str
    SMTP_TLS_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    
    @validator("SERVER_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, value: str | list[str]) -> str | list[str]:
        if isinstance(value, str) and not value.startswith("["):
            return [i.strip() for i in value.split(",")]
        elif isinstance(value, (list, str)):
            return value
        raise ValueError(value)
    
    @validator("MYSQL_DATABASE_URI", pre=True, always=True)
    def assemble_db_connection(cls, value: str | None, values: dict[str, object]) -> object:
        if isinstance(value, str):
            return value
        return f"mysql+aiomysql://{values.get('MYSQL_USER')}:{values.get('MYSQL_PASSWORD')}@{values.get('MYSQL_HOST')}:" \
               f"{values.get('MYSQL_PORT')}/{values.get('MYSQL_DATABASE')}"

    class Config:
        env_file = ".env.local"
        case_sensitive = True

settings = Settings()