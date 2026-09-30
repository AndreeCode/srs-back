from fastapi.responses import JSONResponse

from ..config.config import config

ACCESS_TOKEN_COOKIE = "access_token"
DEVICE_TOKEN_COOKIE = "device_token"
DEVICE_TOKEN_MAX_AGE = 400 * 24 * 60 * 60


def set_auth_cookie(response: JSONResponse, token: str) -> None:
    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE,
        value=token,
        httponly=True,
        secure=config.cookie_secure,
        samesite="lax",
        max_age=config.jwt_expire_minutes * 60,
        path="/",
    )


def clear_auth_cookie(response: JSONResponse) -> None:
    response.delete_cookie(key=ACCESS_TOKEN_COOKIE, path="/")


def set_device_cookie(response: JSONResponse, device_token: str) -> None:
    response.set_cookie(
        key=DEVICE_TOKEN_COOKIE,
        value=device_token,
        httponly=True,
        secure=config.cookie_secure,
        samesite="lax",
        max_age=DEVICE_TOKEN_MAX_AGE,
        path="/",
    )
