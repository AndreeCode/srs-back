from jwt import PyJWTError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from ...modules.session.services.sessions_service import sessionService
from ..db.audit_context import set_audit_context
from ..http.error import error
from .cookies import ACCESS_TOKEN_COOKIE
from .jwt import decode_access_token
from .tokens import hash_token

PUBLIC_PATHS = {
    "/api",
    "/api/auth/login",
    "/api/auth/logout",
    "/docs",
    "/docs/oauth2-redirect",
    "/redoc",
    "/openapi.json",
}


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        token = request.cookies.get(ACCESS_TOKEN_COOKIE)

        if token is None:
            return error(401, "No autenticado", ValueError("missing access_token cookie"))

        try:
            payload = decode_access_token(token)
        except PyJWTError as err:
            return error(401, "Token invalido o expirado", err)

        try:
            session = await sessionService.get_active_by_token(hash_token(token))
        except Exception as err:
            return error(500, "Error al validar la sesion", err)

        if session is None or str(session.user_id) != payload.get("sub"):
            return error(401, "La sesion fue cerrada o ya no es valida", ValueError("session not active"))

        set_audit_context(
            user_id=str(session.user_id),
            device_id=str(session.device_id),
            ip=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )

        request.state.user = payload
        return await call_next(request)
