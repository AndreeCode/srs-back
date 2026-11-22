from datetime import datetime, timedelta
from uuid import UUID

from ....core.config.config import config
from ....core.security import totp
from ....core.security.access_error import AccessDeniedError
from ....core.security.password import verify_password
from ....core.security.secret_box import open_sealed, seal
from ...role.services.roles_service import roleService
from ...session.repositories.session_repositories import sessionRepository
from ...user.repositories.user_repositories import userRepository
from ...user.services.users_service import userService
from ..repositories.auth_event_repository import log_auth_event


class MfaError(ValueError):
    pass


class ReauthLockedError(ValueError):
    def __init__(self, locked_until: datetime):
        super().__init__("cuenta bloqueada")
        self.locked_until = locked_until


def context(user_id) -> str:
    return f"mfa:{user_id}"


def required_for(role_name: str | None) -> bool:
    return config.mfa_required and (role_name or "") in config.mfa_roles


async def role_name(user) -> str | None:
    role = await roleService.get_by_id(user.role_id)
    return role.name if role else None


def temp_password_expires_at(security: dict) -> datetime | None:
    if not security or not security["must_change_password"] or security["password_changed_at"] is None:
        return None
    return security["password_changed_at"] + timedelta(hours=config.temp_password_hours)


async def status(user) -> dict:
    sec = await userRepository.security(user.id)
    required = required_for(await role_name(user))
    return {
        "enabled": bool(sec["mfa_enabled"]),
        "required": required,
        "setup_pending": bool(sec["mfa_pending_secret"]),
        "recovery_codes_left": len(sec["mfa_recovery_codes"] or []) if sec["mfa_enabled"] else 0,
        "enabled_at": sec["mfa_enabled_at"].isoformat() if sec["mfa_enabled_at"] else None,
    }


async def confirm_password(user, password: str) -> None:
    locked_until = await userRepository.locked_until(user.id)
    if locked_until is not None:
        raise ReauthLockedError(locked_until)
    if verify_password(password, user.password_hash):
        return
    locked_until = await userRepository.register_login_failure(
        user.id, config.login_max_attempts, config.login_lock_minutes * 60
    )
    await log_auth_event("LOGIN_FAILED", user.id, "failed", {"reason": "reauth_bad_password"})
    if locked_until is not None:
        await log_auth_event("ACCOUNT_LOCKED", user.id, "blocked", {"reason": "password_guessing"})
        await sessionRepository.revoke_all_of_user(user.id, "password_guessing")
        raise ReauthLockedError(locked_until)
    raise MfaError("La contrasena es incorrecta")


async def setup(user, password: str) -> dict:
    await confirm_password(user, password)
    sec = await userRepository.security(user.id)
    if sec["mfa_enabled"]:
        raise MfaError("La verificacion en dos pasos ya esta activa")
    secret = totp.new_secret()
    await userRepository.set_mfa_pending(user.id, seal(config.mfa_key, secret, context(user.id)))
    return {"secret": secret, "otpauth_uri": totp.provisioning_uri(secret, user.username, config.mfa_issuer)}


async def enable(user_id: UUID, session_id: UUID, code: str) -> list[str]:
    sec = await userRepository.security(user_id)
    if not sec["mfa_pending_secret"]:
        raise MfaError("Primero genera la clave con 'Configurar verificacion en dos pasos'")
    if sec["mfa_enabled"]:
        raise MfaError("La verificacion en dos pasos ya esta activa")
    secret = open_sealed(config.mfa_key, sec["mfa_pending_secret"], context(user_id))
    step = totp.verify(secret, code)
    if step is None:
        raise MfaError("El codigo no es valido. Revisa que la hora del celular sea automatica e intenta de nuevo")
    codes = totp.new_recovery_codes()
    await userRepository.enable_mfa(user_id, sec["mfa_pending_secret"], step, [totp.hash_recovery_code(c) for c in codes])
    await sessionRepository.revoke_all_of_user(user_id, "mfa_enabled", session_id)
    await log_auth_event("MFA_ENABLED", user_id, "successful")
    return codes


async def verify_code(user_id: UUID, code: str) -> bool:
    sec = await userRepository.security(user_id)
    if not sec or not sec["mfa_enabled"] or not sec["mfa_secret"]:
        return False
    secret = open_sealed(config.mfa_key, sec["mfa_secret"], context(user_id))
    step = totp.verify(secret, code, sec["mfa_last_step"])
    if step is not None:
        return await userRepository.set_mfa_step(user_id, step)
    if await userRepository.consume_recovery_code(user_id, totp.hash_recovery_code(code)):
        await log_auth_event("LOGIN", user_id, "successful", {"mfa": "recovery_code"})
        return True
    return False


async def disable(user, session_id: UUID, password: str, code: str) -> None:
    if required_for(await role_name(user)):
        raise AccessDeniedError("Tu rol exige la verificacion en dos pasos: no se puede desactivar")
    await confirm_password(user, password)
    if not await verify_code(user.id, code):
        raise MfaError("El codigo no es valido")
    await userRepository.clear_mfa(user.id)
    await sessionRepository.revoke_all_of_user(user.id, "mfa_disabled", session_id)
    await log_auth_event("MFA_DISABLED", user.id, "successful")


async def reset(caller_id: UUID, user_id: UUID) -> None:
    from ...user.services.user_access_service import ensure_can_manage

    if caller_id == user_id:
        raise AccessDeniedError("Para tu propia cuenta usa 'Verificacion en dos pasos' en el menu")
    target = await userService.get_by_id(user_id)
    if target is None:
        raise MfaError("Usuario no encontrado")
    await ensure_can_manage(caller_id, target)
    await userRepository.clear_mfa(user_id)
    await sessionRepository.revoke_all_of_user(user_id, "mfa_reset")
    await log_auth_event("MFA_RESET", user_id, "successful", {"by": str(caller_id)})
