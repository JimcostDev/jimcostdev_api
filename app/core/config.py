from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    # Estas dos *siempre* vienen de las env vars del sistema:
    MONGO_URI: str = Field(..., env="MONGO_URI")
    JWT_SECRET_KEY:          str = Field(..., env="JWT_SECRET_KEY")

    # Nombre hardcodeado de la base de datos
    MONGODB_NAME: str = "jimcostdev_api"

    # Resto de defaults
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    PROJECT_NAME: str = "JimcostDev API"
    PROJECT_DESCRIPTION: str = (
        "API desarrollada con FastAPI para administrar de manera eficiente mi CV y portafolio profesional."
    )
    PROJECT_VERSION: str = "2.0.0"
    API_PREFIX: str = ""
    CORS_ORIGINS: List[str] = [
        "https://jimcostdev.github.io",
        "https://jimcostdev.com",
        "https://cv.jimcostdev.com",
        "https://jimcostdev-astro.vercel.app",
        "http://localhost:4321/",
    ]

    model_config = SettingsConfigDict(
        env_file=None,   # desactiva carga automática de .env
        extra="ignore",  # ignora cualquier otra var no definidas aquí
    )

settings = Settings()
