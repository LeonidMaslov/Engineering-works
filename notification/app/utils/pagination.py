from math import ceil

from typing import Any, Generic, Optional, Sequence, TypeVar

from fastapi import Query
from pydantic import BaseModel, NonNegativeInt
from typing_extensions import Self

from fastapi_pagination.bases import AbstractPage, AbstractParams, RawParams


class CustomParams(BaseModel, AbstractParams):
    """Кастомный класс параметров запроса для пагинации"""
    page_number: int = Query(1, ge=1, description="Номер страницы")
    page_size: int = Query(20, ge=1, le=100, description="Размер страницы")

    def to_raw_params(self) -> RawParams:
        """Преобразование параметров пагинации для ORM"""
        return RawParams(limit=self.page_size, offset=self.page_size * (self.page_number - 1))


class CustomPageMeta(BaseModel):
    """Кастомный класс для секции 'meta' на странице пагинации"""
    objects_count: NonNegativeInt = 0
    objects_total: NonNegativeInt = 0
    page_number: NonNegativeInt = 0
    pages_count: NonNegativeInt = 0


T = TypeVar("T")


class CustomPage(AbstractPage[T], Generic[T]):
    """Кастомный класс для старицы данных с пагинацией"""
    items: Sequence[T]
    meta: CustomPageMeta

    __params_type__ = CustomParams

    @classmethod
    def create(
            cls,
            items: Sequence[T],
            params: AbstractParams,
            *,
            total: Optional[int] = None,
            **kwargs: Any,
    ) -> Self:
        assert isinstance(params, CustomParams)
        assert total is not None

        page_size = params.page_size if params.page_size is not None else total
        page_number = params.page_number if params.page_number is not None else 1
        pages_count = ceil(total / page_size) if total is not None else None

        return cls(
            items=items,
            meta={
                "objects_count": len(items),
                "objects_total": total,
                "page_number": page_number,
                "pages_count": pages_count
            },
            **kwargs,
        )
