from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

import math

from fastapi import Request
from pydantic import BaseModel, Field

from ....core.config.config import config
from ....core.db.audit_context import set_audit_context, valid_ip
from ....core.http.error import error
from ....core.http.succes import success
from ....core.security.client_ip import client_ip
from ....core.security.cookies import DEVICE_TOKEN_COOKIE, set_auth_cookie, set_device_cookie
from jwt import PyJWTError

from ....core.security.jwt import create_access_token, create_mfa_token, decode_mfa_token
from ....core.security.password import burn_password_check, hash_password, needs_rehash, verify_password
from ....core.security.tokens import generate_token, hash_token
from ....core.logger.logger import logger
from ...device.services.devices_service import deviceService
from ...role.services.roles_service import roleService
from ...security_alert.services.security_alerts_service import securityAlertService
from ...session.domain.session_domain import Session
from ...session.services.sessions_service import sessionService
from ...user.repositories.user_repositories import userRepository
from ...user.services.users_service import userService
from ..repositories.auth_event_repository import log_auth_event
from ..services import auth_mfa_service as mfa
from ...security_alert.services.security_alerts_service import securityAlertService as alerts
from .login_rate_limiter import allow_login_attempt, register_unknown_login_failure, unknown_login_locked_until


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=150)
    password: str = Field(min_length=1, max_length=128)


class MfaLoginRequest(BaseModel):
    mfa_token: str = Field(min_length=10, max_length=2000)
    code: str = Field(min_length=6, max_length=20)


NIL_USER = UUID(int=0)


def lock_message(until: datetime) -> str:
    minutes = max(1, math.ceil((until - datetime.now(timezone.utc)).total_seconds() / 60))
    return f"La cuenta esta bloqueada temporalmente por intentos fallidos. Intenta nuevamente en {minutes} minuto(s)"


async def check_credentials(body: LoginRequest):
    user = await userService.get_by_username(body.username)

    if user is None:
        locked_until = unknown_login_locked_until(body.username)
        if locked_until is not None:
            await userRepository.locked_until(NIL_USER)
            await log_auth_event("LOGIN_FAILED", None, "blocked", {"username": body.username, "reason": "locked"})
            return None, error(429, lock_message(locked_until), ValueError("locked unknown user"))
        await userRepository.locked_until(NIL_USER)
        burn_password_check(body.password)
        await userRepository.register_login_failure(NIL_USER, config.login_max_attempts, config.login_lock_minutes * 60)
        locked_until = register_unknown_login_failure(body.username)
        await log_auth_event("LOGIN_FAILED", None, "failed", {"username": body.username, "reason": "unknown_user"})
        if locked_until is not None:
            await log_auth_event("ACCOUNT_LOCKED", None, "blocked", {"username": body.username})
            await alerts.scan_auth(None)
            return None, error(429, lock_message(locked_until), ValueError("unknown user locked"))
        return None, error(401, "Usuario o contrasena incorrectos", ValueError("invalid credentials"))

    locked_until = await userRepository.locked_until(user.id)
    if locked_until is not None:
        await log_auth_event("LOGIN_FAILED", user.id, "blocked", {"username": body.username, "reason": "locked"})
        return None, error(429, lock_message(locked_until), ValueError(f"user_id={user.id} locked"))

    if not verify_password(body.password, user.password_hash):
        locked_until = await userRepository.register_login_failure(
            user.id, config.login_max_attempts, config.login_lock_minutes * 60
        )
        await log_auth_event("LOGIN_FAILED", user.id, "failed", {"username": body.username, "reason": "bad_password"})
        if locked_until is not None:
            await log_auth_event("ACCOUNT_LOCKED", user.id, "blocked", {"username": body.username})
            await alerts.scan_auth(user.id)
            return None, error(429, lock_message(locked_until), ValueError(f"user_id={user.id} locked"))
        return None, error(401, "Usuario o contrasena incorrectos", ValueError("invalid credentials"))

    await userRepository.reset_login_failures(user.id)
    return user, None


async def login_handler(request: Request, body: LoginRequest):
    try:
        set_audit_context(ip=client_ip(request), user_agent=request.headers.get("user-agent"))
        if not allow_login_attempt(client_ip(request)):
            await log_auth_event("LOGIN_FAILED", None, "blocked", {"username": body.username, "reason": "ip_rate_limit"})
            await alerts.scan_auth(None)
            return error(429, "Demasiados intentos de inicio de sesion, espera un minuto", ValueError("ip rate limit"))

        user, failure = await check_credentials(body)
        if failure is not None:
            return failure

        if not user.active:
            await log_auth_event("LOGIN_FAILED", user.id, "blocked", {"reason": "inactive"})
            return error(403, "El usuario esta inactivo", ValueError(f"user_id={user.id}"))

        if user.blocked:
            reason = f": {user.blocked_reason}" if user.blocked_reason else ""
            await log_auth_event("LOGIN_FAILED", user.id, "blocked", {"reason": "blocked"})
            return error(403, f"La cuenta esta bloqueada{reason}", ValueError(f"user_id={user.id}"))

        security = await userRepository.security(user.id)
        expires = mfa.temp_password_expires_at(security)
        if expires is not None and expires < datetime.now(timezone.utc):
            await log_auth_event("LOGIN_FAILED", user.id, "blocked", {"reason": "temp_password_expired"})
            return error(403, "Tu contrasena temporal vencio. Pide a un administrador que la restablezca", ValueError("temp expired"))

        if security["mfa_enabled"]:
            return success(
                200,
                "Ingresa el codigo de tu app autenticadora",
                {"mfa_required": True, "mfa_token": create_mfa_token(str(user.id))},
            )

        return await start_session(request, user, body.password)

    except Exception as err:
        return error(500, "Error al iniciar sesion", err)


async def mfa_login_handler(request: Request, body: MfaLoginRequest):
    try:
        ip = client_ip(request)
        set_audit_context(ip=ip, user_agent=request.headers.get("user-agent"))
        if not allow_login_attempt(ip):
            return error(429, "Demasiados intentos de inicio de sesion, espera un minuto", ValueError("ip rate limit"))
        try:
            user_id = UUID(decode_mfa_token(body.mfa_token)["sub"])
        except (PyJWTError, ValueError) as err:
            return error(401, "La verificacion vencio, vuelve a ingresar tu usuario y contrasena", err)
        user = await userService.get_by_id(user_id)
        if user is None or not user.active or user.blocked:
            return error(403, "La cuenta no esta habilitada", ValueError(f"user_id={user_id}"))
        locked_until = await userRepository.locked_until(user.id)
        if locked_until is not None:
            return error(429, lock_message(locked_until), ValueError("locked"))
        if not await mfa.verify_code(user.id, body.code):
            locked_until = await userRepository.register_login_failure(
                user.id, config.login_max_attempts, config.login_lock_minutes * 60
            )
            await log_auth_event("MFA_FAILED", user.id, "failed")
            if locked_until is not None:
                await log_auth_event("ACCOUNT_LOCKED", user.id, "blocked", {"reason": "mfa_guessing"})
                await alerts.scan_auth(user.id)
                return error(429, lock_message(locked_until), ValueError("mfa locked"))
            return error(401, "El codigo de verificacion no es valido", ValueError("bad mfa code"))
        await userRepository.reset_login_failures(user.id)
        return await start_session(request, user, None)

    except Exception as err:
        return error(500, "Error al iniciar sesion", err)


async def start_session(request: Request, user, password: str | None):
    try:
        ip = client_ip(request)
        user_agent = request.headers.get("user-agent")
        set_audit_context(user_id=str(user.id), ip=ip, user_agent=user_agent)

        device_token = request.cookies.get(DEVICE_TOKEN_COOKIE) or generate_token()
        device = await deviceService.register(user.id, hash_token(device_token), user_agent)

        if not device.trusted:
            what = "Este navegador esta bloqueado" if device.block_scope == "browser" else "Este dispositivo esta bloqueado para la cuenta"
            reason = f": {device.blocked_reason}" if device.blocked_reason else ""
            await log_auth_event("LOGIN_FAILED", user.id, "blocked", {"reason": "device_blocked", "device_id": str(device.id)})
            return error(403, f"{what}{reason}", ValueError(f"device_id={device.id}"))

        set_audit_context(device_id=str(device.id))

        if password is not None and needs_rehash(user.password_hash):
            await userRepository.rehash_password(user.id, hash_password(password))

        session_id = uuid4()
        token = create_access_token(
            {
                "sub": str(user.id),
                "username": user.username,
                "role_id": str(user.role_id),
                "sid": str(session_id),
                "did": str(device.id),
            }
        )

        await sessionService.create(
            Session(
                id=session_id,
                user_id=user.id,
                device_id=device.id,
                token_hash=hash_token(token),
                ip_address=valid_ip(ip),
                expires_at=datetime.now(timezone.utc) + timedelta(minutes=config.jwt_expire_minutes),
            )
        )

        try:
            await securityAlertService.scan(device_hash=device.device_hash, user_id=user.id)
        except Exception as err:
            logger.error(f"No se pudo revisar la actividad del login: {err}")

        await log_auth_event("LOGIN", user.id, "successful", {"session_id": str(session_id)})

        role = await roleService.get_by_id(user.role_id)
        response = success(200, "Inicio de sesion exitoso", {**user.to_dict(), "role": role.name if role else None})
        set_auth_cookie(response, token)
        set_device_cookie(response, device_token)
        return response

    except Exception as err:
        return error(500, "Error al iniciar sesion", err)
