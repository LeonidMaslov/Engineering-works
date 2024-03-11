import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Security, Header, status, responses
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.async_sqlalchemy import paginate

from database import postgres, logic
from schemas import admin, response
from core.exceptions.schemas import errors
from utils.filters import AdminNotificationFilter
from utils.pagination import CustomPage
from core.security.validation import token_key

router = APIRouter()


@router.post("/",
             description="Создание уведомления администратором",
             dependencies=[Security(token_key)],
             response_model=admin.AdminRetrieveNotification,
             responses={400: {'model': errors.PydanticError}})
async def create_notification(notification_data: admin.AdminCreateNotification,
                              user_id: uuid.UUID = Header(description="Идентификатор пользователя в auth service"),
                              session: AsyncSession = Depends(postgres.get_session)):
    """
    Создание уведомления администратором
    :param notification_data: Данные для создания уведомления
    :param user_id: Идентификатор пользователя в auth service в формате UUID
    :param session: Сессия для работы с базой данных
    :return: Данные уведомления или сообщение об ошибке
    """
    return await logic.create_notification(session, user_id, notification_data)


@router.get("/notifications",
            description="Получение списка уведомлений администратором с пагинацией и фильтрацией",
            response_model=CustomPage[admin.AdminRetrieveListNotification])
async def get_notifications_list(
        notification_filters: AdminNotificationFilter = FilterDepends(AdminNotificationFilter),
        session: AsyncSession = Depends(postgres.get_session)) -> CustomPage[admin.AdminRetrieveListNotification]:
    """
    Получение списка уведомлений администратором с пагинацией и фильтрацией
    :param notification_filters: Фильтры уведомлений
    :param session: Сессия для работы с базой данных
    :return: Список уведомлений или пустой список
    """
    return await paginate(session, logic.get_filtered_notifications(notification_filters))


@router.get("/{notification_id}",
            description="Получение уведомления администратором по ID",
            response_model=admin.AdminRetrieveNotification,
            responses={404: {'model': errors.NotFoundNotificationError}})
async def get_notification_by_id(notification_id: uuid.UUID, session: AsyncSession = Depends(postgres.get_session)):
    """
    Получение уведомления администратором по ID
    :param notification_id: Идентификатор уведомления в формате UUID
    :param session: Сессия для работы с базой данных
    :return: Уведомление или ошибка 404
    """
    return await logic.get_notification_or_404(session, notification_id)


@router.patch("/{notification_id}",
              description="Изменение уведомления по ID администратором ",
              dependencies=[Security(token_key)],
              response_model=admin.AdminRetrieveNotification,
              responses={400: {'model': errors.PydanticError},
                         404: {'model': errors.NotFoundNotificationError}})
async def update_notification_by_id(
        notification_id: uuid.UUID,
        notification_data: admin.AdminUpdateNotification,
        user_id: uuid.UUID = Header(description="Идентификатор пользователя в auth service"),
        session: AsyncSession = Depends(postgres.get_session)):
    """
    Изменение уведомления по ID администратором
    :param notification_id: Идентификатор уведомления в формате UUID
    :param notification_data: Данные для обновления в уведомлении
    :param user_id: Идентификатор пользователя в auth service в формате UUID
    :param session: Сессия для работы с базой данных
    :return: Измененное уведомление или уведомление об ошибке
    """
    return await logic.update_notification(session, user_id, notification_id, notification_data)


@router.delete("/{notification_id}",
               description="Удаление уведомления администратором",
               dependencies=[Security(token_key)],
               responses={200: {"model": response.SuccessfulResponse},
                          404: {"model": errors.NotFoundNotificationError}})
async def delete_notification_by_id(
        notification_id: uuid.UUID,
        notification_data: admin.AdminDeleteNotification,
        user_id: uuid.UUID = Header(description="Идентификатор пользователя в auth service"),
        session: AsyncSession = Depends(postgres.get_session)):
    """
    Удаление уведомления администратором
    :param notification_id: Идентификатор уведомления в формате UUID
    :param notification_data: Данные для обновления в уведомлении
    :param user_id: Идентификатор пользователя в auth service в формате UUID
    :param session: Сессия для работы с базой данных
    :return: Успешный ответ или уведомление об ошибке
    """
    await logic.delete_notification(session, user_id, notification_id, notification_data)
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=response.SuccessfulResponse().dict())
