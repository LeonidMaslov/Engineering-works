import uuid
from datetime import datetime
from typing import Sequence

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select

from models import Notification
from schemas import admin
from core import exceptions
from core.exceptions.schemas import errors
from utils.filters import AdminNotificationFilter
from core.settings import settings


def _select_not_deleted_notification() -> Select[tuple[Notification]]:
    """
    Генерация запроса для получения уведомлений
    :return: Запрос на получение уведомлений с флагом is_deleted == False
    """
    return (
        sa.select(Notification).
        filter(Notification.is_deleted == False)
    )


def _select_published_notifications() -> Select[tuple[Notification]]:
    """
    Получение опубликованных уведомлений
    :return: Запрос на получение опубликованные уведомления
    """
    now = datetime.utcnow()
    return (
        _select_not_deleted_notification().
        filter(
            sa.and_(
                Notification.start_date <= now,
                sa.or_(
                    Notification.end_date >= now,
                    Notification.end_date == None
                )
            )
        )
    )


def _select_technical_notifications(*filters, **kw_filters) -> Select[tuple[Notification]]:
    return (
        _select_not_deleted_notification().
        where(Notification.type == settings.TECHNICAL_WORKS_NOTIFICATION_TYPE, *filters, **kw_filters)
    )


async def _check_exists_technical_notification(session: AsyncSession, *filters, **kw_filters) -> bool:
    """
    Проверка наличия системных записей по заданным фильтрам
    :param session: Сессия для работы с базой данных
    :param filters: Фильтры для поиска записей
    :param kw_filters: Фильтры для поиска записей в формате `ключ=значение`
    :return: Логическое значение существования записи
    """
    technical_notification = await session.execute(_select_technical_notifications(*filters, **kw_filters))
    if len(technical_notification.scalars().all()) > 0:
        return True

    return False


async def get_technical_notification(session: AsyncSession) -> Sequence[Notification]:
    """
    Получение технических уведомлений
    :param session: Сессия для работы с базой данных
    :return: Список технических уведомлений
    """
    query = _select_technical_notifications()
    result = await session.execute(query)
    return result.scalars().all()


async def get_published_notifications(session: AsyncSession) -> Sequence[Notification]:
    """
    Получение списка опубликованных уведомлений
    :param session: Сессия для работы с базой данных
    :return: Список опубликованных уведомлений
    """
    query = _select_published_notifications()
    result = await session.execute(query)
    return result.scalars().all()


def get_filtered_notifications(filters: AdminNotificationFilter) -> Select:
    """
    Фильтрация уведомлений
    :param filters: Класс для фильтрации уведомлений
    :return: Запрос на получение уведомлений с фильтрами
    """
    return filters.filter(_select_not_deleted_notification())


async def get_notification_or_404(session: AsyncSession, notification_id: uuid.UUID) -> Notification:
    """
    Получение уведомления по ID
    :param session: Сессия для работы с базой данных
    :param notification_id: Идентификатор уведомления в формате UUID
    :return: Уведомление или ошибка 404
    """
    query = _select_not_deleted_notification().where(Notification.id == notification_id)
    result = await session.execute(query)
    notification = result.scalars().first()

    if not notification:
        raise exceptions.NotFoundHTTPException(errors.NotFoundNotificationError())

    return notification


async def create_notification(session: AsyncSession,
                              user_id: uuid.UUID,
                              notification_data: admin.AdminCreateNotification) -> Notification:
    """
    Создание уведомления
    :param session: Сессия для работы с базой данных
    :param user_id: Идентификатор пользователя в auth service в формате UUID
    :param notification_data: Данные для создания уведомления
    :return: Созданное уведомление
    """
    # Реализация требования существования одного системного уведомления в единицу времени.
    # TODO Удалить, когда требования существования одного системного уведомления пропадет
    is_technical_notification_exists = await _check_exists_technical_notification(session)

    if notification_data.type == settings.TECHNICAL_WORKS_NOTIFICATION_TYPE and is_technical_notification_exists:
        raise exceptions.ValidationHTTPException(errors.TechnicalWorksDuplicateError())

    notification_data.audit_info.creator.sidecar_id = user_id.__str__()

    notification = Notification(**notification_data.model_dump())

    try:
        session.add(notification)
    except IntegrityError:
        raise exceptions.ValidationHTTPException(errors.DuplicateNotificationError())

    await session.commit()

    return notification


async def update_notification(session: AsyncSession,
                              user_id: uuid.UUID,
                              notification_id: uuid.UUID,
                              notification_data: admin.AdminUpdateNotification) -> Notification:
    """
    Обновление уведомления по ID
    :param session: Сессия для работы с базой данных
    :param user_id: Идентификатор пользователя в auth service в формате UUID
    :param notification_id:
    :param notification_data: Данные для обновления уведомления
    :return: Обновленное уведомление
    """
    # Реализация требования существования одного системного уведомления в единицу времени.
    # TODO Удалить, когда требования существования одного системного уведомления пропадет
    is_technical_notification_exists = await _check_exists_technical_notification(
        session,
        sa.not_(Notification.id == notification_id)
    )

    if notification_data.type == settings.TECHNICAL_WORKS_NOTIFICATION_TYPE and is_technical_notification_exists:
        raise exceptions.ValidationHTTPException(errors.TechnicalWorksDuplicateError())

    notification = await get_notification_or_404(session, notification_id)

    notification_data.audit_info.updater.sidecar_id = user_id.__str__()
    notification.audit_info.update(updater=notification_data.audit_info.updater.model_dump())

    for key, value in notification_data.model_dump(exclude={"audit_info"}, exclude_none=True).items():
        if notification.__getattribute__(str(key)):
            setattr(notification, key, value)

    await session.commit()

    return notification


async def delete_notification(session: AsyncSession,
                              user_id: uuid.UUID,
                              notification_id: uuid.UUID,
                              notification_data: admin.AdminDeleteNotification) -> Notification:
    """
    Удаление уведомления.
    Устанавливает статус `is_deleted` как `True` и записывает данные о пользователе, удалившем уведомление
    :param session: Сессия для работы с базой данных
    :param user_id: Идентификатор пользователя в auth service в формате UUID
    :param notification_id:
    :param notification_data: Данные для обновления уведомления
    :return: Данные удаленного уведомление
    """
    notification = await get_notification_or_404(session, notification_id)

    notification_data.audit_info.deleter.sidecar_id = user_id.__str__()
    notification.audit_info.update(deleter=notification_data.audit_info.deleter.model_dump())
    notification.is_deleted = True

    await session.commit()

    return notification
