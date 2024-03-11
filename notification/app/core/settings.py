from pydantic import BaseModel

from pydantic_settings import BaseSettings


class LoggingConfig(BaseModel):
    """Конфигурация логирования для FastAPI сервера"""

    LOGGER_NAME: str = "blogs"
    LOG_FORMAT: str = "%(levelprefix)s [%(asctime)s] %(message)s"
    LOG_LEVEL: str = "INFO"

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers: dict = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }


class Settings(BaseSettings):
    """Класс с настройками сервиса"""
    PROJECT_NAME: str = 'Notification'
    API_V1_STR: str = "/api"
    SERVICE_PREFIX: str = '/notification'

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    LOGGING_CONFIG: LoggingConfig = LoggingConfig()

    TECHNICAL_WORKS_NOTIFICATION_TYPE: str = "sys"

    @property
    def postgres_db_url(self):
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'


settings = Settings()
