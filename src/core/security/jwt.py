from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from ..config.config import config

ISSUER = "sicna"
AUDIENCE = "sicna-api"
MFA_AUDIENCE = "sicna-mfa"
MFA_TOKEN_MINUTES = 5


def create_access_token(data: dict[str, Any]) -> str:
    now = datetime.now(timezone.utc)
    payload = {**data, "iss": ISSUER, "aud": AUDIENCE, "iat": now, "exp": now + timedelta(minutes=config.jwt_expire_minutes)}
    return jwt.encode(payload, config.jwt_secret, algorithm=config.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        token,
        config.jwt_secret,
        algorithms=[config.jwt_algorithm],
        issuer=ISSUER,
        audience=AUDIENCE,
        options={"require": ["exp", "iat", "iss", "aud", "sub", "sid"]},
    )


def create_mfa_token(user_id: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {"sub": user_id, "iss": ISSUER, "aud": MFA_AUDIENCE, "iat": now, "exp": now + timedelta(minutes=MFA_TOKEN_MINUTES)}
    return jwt.encode(payload, config.jwt_secret, algorithm=config.jwt_algorithm)


def decode_mfa_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        token,
        config.jwt_secret,
        algorithms=[config.jwt_algorithm],
        issuer=ISSUER,
        audience=MFA_AUDIENCE,
        options={"require": ["exp", "sub", "aud", "iss"]},
    )
