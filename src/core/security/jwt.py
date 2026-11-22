from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from ..config.config import config

ISSUER = "sicna"


def create_access_token(data: dict[str, Any]) -> str:
    now = datetime.now(timezone.utc)
    payload = {**data, "iss": ISSUER, "iat": now, "exp": now + timedelta(minutes=config.jwt_expire_minutes)}
    return jwt.encode(payload, config.jwt_secret, algorithm=config.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        token,
        config.jwt_secret,
        algorithms=[config.jwt_algorithm],
        issuer=ISSUER,
        options={"require": ["exp", "iat", "iss", "sub", "sid"]},
    )
