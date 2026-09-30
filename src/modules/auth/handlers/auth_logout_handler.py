from fastapi import Request
from jwt import PyJWTError

from ....core.db.audit_context import set_audit_context
from ....core.http.succes import success
from ....core.logger.logger import logger
from ....core.security.cookies import ACCESS_TOKEN_COOKIE, clear_auth_cookie
from ....core.security.jwt import decode_access_token
from ....core.security.tokens import hash_token
from ...session.services.sessions_service import sessionService


async def logout_handler(request: Request):
    token = request.cookies.get(ACCESS_TOKEN_COOKIE)

    if token is not None:
        try:
            payload = decode_access_token(token)
            set_audit_context(
                user_id=payload.get("sub"),
                device_id=payload.get("did"),
                ip=request.client.host if request.client else None,
                user_agent=request.headers.get("user-agent"),
            )
            await sessionService.revoke_by_token(hash_token(token), "logout")
        except PyJWTError:
            pass
        except Exception as err:
            logger.error(f"No se pudo cerrar la sesion en la base de datos: {err}")

    response = success(200, "Sesion cerrada correctamente")
    clear_auth_cookie(response)
    return response
