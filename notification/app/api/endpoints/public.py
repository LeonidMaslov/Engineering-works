import uuid
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Header

from database import postgres, logic
from schemas import user
from core.exceptions.schemas import errors

router = APIRouter()


@router.get("/",
            description="Получение списка опубликованных уведомлений для внешних пользователей",
            response_model=List[user.UserNotification],
            responses={400: {'model': errors.PydanticError}})
async def get_public_published_notifications(
        user_id: uuid.UUID = Header(description="Идентификатор пользователя в auth service", default=None),
        session_id: str = Header(description="Идентификатор сессии браузера", default=None),
        session: AsyncSession = Depends(postgres.get_session)):
    """
    Получение списка опубликованных уведомлений для внешних пользователей
    :param user_id: Идентификатор пользователя в auth service в формате UUID
    :param session_id: Идентификатор сессии браузера
    :param session: Сессия для работы с базой данных
    :return: Список опубликованных уведомлений
    """
    if not user_id:
        return await logic.get_technical_notification(session)

    return await logic.get_published_notifications(session)
