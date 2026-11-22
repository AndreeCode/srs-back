from datetime import datetime, timedelta, timezone
from uuid import uuid4

from fastapi import Request
from pydantic import BaseModel

from ....core.config.config import config
from ....core.db.audit_context import set_audit_context, valid_ip
from ....core.http.error import error
from ....core.http.succes import success
from ....core.security.client_ip import client_ip
from ....core.security.cookies import DEVICE_TOKEN_COOKIE, set_auth_cookie, set_device_cookie
from ....core.security.jwt import create_access_token
from ....core.security.password import hash_password, needs_rehash, verify_password
from ....core.security.tokens import generate_token, hash_token
from ....core.logger.logger import logger
from ...device.services.devices_service import deviceService
from ...role.services.roles_service import roleService
from ...security_alert.services.security_alerts_service import securityAlertService
from ...session.domain.session_domain import Session
from ...session.services.sessions_service import sessionService
from ...user.repositories.user_repositories import userRepository
from ...user.services.users_service import userService


class LoginRequest(BaseModel):
    username: str
    password: str


async def login_handler(request: Request, body: LoginRequest):
    try:
        user = await userService.get_by_username(body.username)

        if user is None or not verify_password(body.password, user.password_hash):
            return error(401, "Usuario o contrasena incorrectos", ValueError("invalid credentials"))

        if not user.active:
            return error(403, "El usuario esta inactivo", ValueError(f"user_id={user.id}"))

        if user.blocked:
            reason = f": {user.blocked_reason}" if user.blocked_reason else ""
            return error(403, f"La cuenta esta bloqueada{reason}", ValueError(f"user_id={user.id}"))

        ip = client_ip(request)
        user_agent = request.headers.get("user-agent")
        set_audit_context(user_id=str(user.id), ip=ip, user_agent=user_agent)

        device_token = request.cookies.get(DEVICE_TOKEN_COOKIE) or generate_token()
        device = await deviceService.register(user.id, hash_token(device_token), user_agent)

        if not device.trusted:
            what = "Este navegador esta bloqueado" if device.block_scope == "browser" else "Este dispositivo esta bloqueado para la cuenta"
            reason = f": {device.blocked_reason}" if device.blocked_reason else ""
            return error(403, f"{what}{reason}", ValueError(f"device_id={device.id}"))

        set_audit_context(device_id=str(device.id))

        if needs_rehash(user.password_hash):
            await userRepository.rehash_password(user.id, hash_password(body.password))

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

        role = await roleService.get_by_id(user.role_id)
        response = success(200, "Inicio de sesion exitoso", {**user.to_dict(), "role": role.name if role else None})
        set_auth_cookie(response, token)
        set_device_cookie(response, device_token)
        return response

    except Exception as err:
        return error(500, "Error al iniciar sesion", err)
