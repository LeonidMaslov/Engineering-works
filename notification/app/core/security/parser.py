import logging
import jwt

from fastapi import HTTPException

from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, InvalidAudienceError

from core.security.schemas.token import TokenData

logger = logging.getLogger("blogs")


def parse_keycloak_token(access_token: str) -> TokenData:
    """
    Парсинг токена keycloak
    :param access_token: закодированный токен
    :return: Данные, закодированные в токен
    """
    try:
        decoded_token = jwt.decode(access_token, algorithms="HS256", options={"verify_signature": False})
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Signature has expired")
    except InvalidSignatureError:
        raise HTTPException(status_code=401, detail="Signature verification failed")
    except InvalidAudienceError:
        raise HTTPException(status_code=401, detail="Invalid audience")
    except:
        logger.exception("Unexpected error")
        raise HTTPException(status_code=401, detail="Invalid token")
    return TokenData.model_validate(decoded_token)
