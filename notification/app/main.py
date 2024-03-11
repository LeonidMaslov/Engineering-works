import logging
from logging.config import dictConfig

from fastapi import FastAPI, Request, status
from fastapi_pagination import add_pagination
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api.routers import api_router
from core.settings import settings

dictConfig(settings.LOGGING_CONFIG.dict())

logger = logging.getLogger("uvicorn")

app = FastAPI(
    title=settings.PROJECT_NAME,
    redoc_url=f'{settings.SERVICE_PREFIX}/redoc',
    docs_url=f'{settings.SERVICE_PREFIX}/docs',
    openapi_url=f'{settings.SERVICE_PREFIX}/openapi.json',
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Перехват ошибок валидации и замена кода 422 на кол 400
    :param request: Данные запроса
    :param exc: Ошибка валидации
    :return: JSON ответ
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )

add_pagination(app)

app.include_router(api_router, prefix=f'{settings.SERVICE_PREFIX}{settings.API_V1_STR}')
