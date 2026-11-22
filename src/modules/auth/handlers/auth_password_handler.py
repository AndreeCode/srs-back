from uuid import UUID

from fastapi import Request
from pydantic import BaseModel, Field

from ....core.config.config import config
from ....core.http.error import error
from ....core.http.succes import success
from ....core.security.password import hash_password, verify_password
from ....core.security.password_policy import PasswordPolicyError, ensure_strong_password
from ...session.repositories.session_repositories import sessionRepository
from ...user.repositories.user_repositories import userRepository
from ...user.services.users_service import userService
from .auth_login_handler import lock_message


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=1, max_length=128)
    new_password: str = Field(min_length=1, max_length=128)


async def change_password_handler(request: Request, body: ChangePasswordRequest):
    try:
        user_id = UUID(request.state.user["sub"])
        session_id = UUID(request.state.user["sid"])
        user = await userService.get_by_id(user_id)

        if user is None:
            return error(404, "Usuario no encontrado", ValueError(f"user_id={user_id}"))

        if not verify_password(body.current_password, user.password_hash):
            locked_until = await userRepository.register_login_failure(
                user.id, config.login_max_attempts, config.login_lock_minutes * 60
            )
            if locked_until is not None:
                await sessionRepository.revoke_all_of_user(user.id, "password_guessing")
                return error(429, lock_message(locked_until), ValueError(f"user_id={user.id} locked"))
            return error(400, "La contrasena actual es incorrecta", ValueError("wrong current password"))

        if body.new_password == body.current_password:
            return error(400, "La nueva contrasena debe ser distinta a la actual", ValueError("same password"))

        ensure_strong_password(body.new_password, user.username, user.dni)
        await userRepository.set_password(user.id, hash_password(body.new_password))
        closed = await sessionRepository.revoke_all_of_user(user.id, "password_changed", session_id)
        detail = "" if not closed else ". Se cerro tu otra sesion" if closed == 1 else f". Se cerraron tus otras {closed} sesiones"
        return success(200, f"Contrasena actualizada correctamente{detail}")

    except PasswordPolicyError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al cambiar la contrasena", err)
