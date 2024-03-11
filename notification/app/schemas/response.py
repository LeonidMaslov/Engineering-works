from pydantic import BaseModel


class SuccessfulResponse(BaseModel):
    """Модель успешного ответа"""
    status: str = "successful"
