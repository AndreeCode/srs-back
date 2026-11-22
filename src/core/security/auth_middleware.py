from datetime import datetime, timedelta, timezone

from jwt import PyJWTError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from ...modules.auth.repositories.auth_event_repository import log_auth_event
from ...modules.session.repositories.session_repositories import sessionRepository
from ..config.config import config
from ..db.audit_context import set_audit_context
from ..http.error import error
from .client_ip import client_ip
from .cookies import ACCESS_TOKEN_COOKIE
from .jwt import decode_access_token
from .tokens import hash_token

PUBLIC_PATHS = {"/api", "/api/auth/login", "/api/auth/login/mfa", "/api/auth/logout", "/api/auth/register"}
if not config.is_production:
    PUBLIC_PATHS |= {"/docs", "/docs/oauth2-redirect", "/redoc", "/openapi.json"}


PASSWORD_CHANGE_PATHS = {"/api/auth/me", "/api/auth/password"}
MFA_SETUP_PATHS = {"/api/auth/me", "/api/auth/password", "/api/auth/mfa", "/api/auth/mfa/setup", "/api/auth/mfa/enable"}
TOUCH_EVERY = timedelta(seconds=60)


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
            session = await sessionRepository.access(hash_token(token))
        except Exception as err:
            return error(500, "Error al validar la sesion", err)

        if session is None or str(session["user_id"]) != payload.get("sub"):
            return error(401, "La sesion fue cerrada o ya no es valida", ValueError("session not active"))

        set_audit_context(
            user_id=str(session["user_id"]),
            device_id=str(session["device_id"]),
            ip=client_ip(request),
            user_agent=request.headers.get("user-agent"),
        )

        now = datetime.now(timezone.utc)
        if config.session_idle_minutes > 0 and session["last_activity_at"] < now - timedelta(minutes=config.session_idle_minutes):
            await sessionRepository.revoke_idle(session["id"])
            await log_auth_event(
                "SESSION_IDLE", session["user_id"], "successful",
                {"session_id": str(session["id"]), "idle_minutes": config.session_idle_minutes},
            )
            return error(401, "Tu sesion se cerro por inactividad, vuelve a ingresar", ValueError("idle timeout"))
        if session["last_activity_at"] < now - TOUCH_EVERY:
            await sessionRepository.touch(session["id"])

        path = request.url.path
        if session["must_change_password"] and path not in PASSWORD_CHANGE_PATHS:
            return error(403, "Debes cambiar tu contrasena temporal antes de continuar", ValueError("must change password"))
        if (
            config.mfa_required
            and session["role_name"] in config.mfa_roles
            and not session["mfa_enabled"]
            and path not in MFA_SETUP_PATHS
        ):
            return error(403, "Tu rol exige la verificacion en dos pasos: activala para continuar", ValueError("mfa setup"))

        request.state.user = payload
        response = await call_next(request)
        if response.status_code == 403:
            await log_auth_event(
                "ACCESS_DENIED", session["user_id"], "blocked", {"method": request.method, "path": path}
            )
        return response
