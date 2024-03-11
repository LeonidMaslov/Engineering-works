from datetime import datetime, timezone

from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.security.parser import parse_keycloak_token
from core.security.schemas.token import TokenData

token_key = HTTPBearer()


def validate_token(authorization_token: HTTPAuthorizationCredentials = Security(token_key)) -> TokenData:
    """
    Валидация токена keycloak
    :param authorization_token:
    :return: Данные валидного токена или ошибка валидации токена
    """
    token_data = parse_keycloak_token(authorization_token.credentials)

    if datetime.now(timezone.utc).timestamp() >= token_data.exp:
        raise HTTPException(status_code=401, detail="Token expired.")

    return token_data
