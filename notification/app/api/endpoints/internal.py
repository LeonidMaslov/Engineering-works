import uuid
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Security, Header

from database import postgres, logic
from schemas import user
from core.exceptions.schemas import errors
from core.security.validation import token_key

router = APIRouter()


@router.get("/",
            description="Получение списка опубликованных уведомлений пользователем для внутренних пользователей",
            dependencies=[Security(token_key)],
            response_model=List[user.UserNotification],
            responses={400: {'model': errors.PydanticError}})
async def get_internal_published_notifications(
        user_id: uuid.UUID = Header(description="Идентификатор пользователя в auth service"),
        session_id: str = Header(description="Идентификатор сессии браузера", default=None),
        session: AsyncSession = Depends(postgres.get_session)):
    """
    Получение списка опубликованных уведомлений пользователем для внутренних пользователей
    :param user_id: Идентификатор пользователя в auth service в формате UUID
    :param session_id: Идентификатор сессии браузера
    :param session: Сессия для работы с базой данных
    :return: Список опубликованных уведомлений
    """
    return await logic.get_published_notifications(session)
