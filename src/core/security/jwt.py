from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from ..config.config import config


def create_access_token(data: dict[str, Any]) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=config.jwt_expire_minutes)
    payload = {**data, "exp": expire}
    return jwt.encode(payload, config.jwt_secret, algorithm=config.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, config.jwt_secret, algorithms=[config.jwt_algorithm])
