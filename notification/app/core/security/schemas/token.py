from typing import List, Optional

from pydantic import BaseModel, Field, AnyHttpUrl


class Role(BaseModel):
    """Модель ролей токена"""
    roles: List[str]


class ResourceAccess(BaseModel):
    """Модель ресурсов токена"""
    cpe_as_web_p: Role = Field(alias='cpe-as-web-p')
    account: Role


class TokenData(BaseModel):
    """Модель токена Keycloak"""

    exp: int
    iat: int
    auth_time: Optional[int] = None
    jti: str = None
    iss: AnyHttpUrl = None
    aud: List[str]
    sub: str
    typ: str
    azp: str

    nonce: str
    session_state: str
    acr: str

    allowed_origins: List[str] = Field(alias='allowed-origins')
    realm_access: Role
    resource_access: dict

    scope: str
    sid: str
    email_verified: bool
    name: str
    preferred_username: str
    given_name: str
    middle_name: str = None
    family_name: str
    email: str
