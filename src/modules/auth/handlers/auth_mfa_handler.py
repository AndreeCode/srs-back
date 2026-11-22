from uuid import UUID

from fastapi import Request
from pydantic import BaseModel, Field

from ....core.http.error import error
from ....core.http.succes import success
from ....core.security.access_error import AccessDeniedError
from ...session.repositories.session_repositories import sessionRepository
from ...user.services.users_service import userService
from ..repositories.auth_event_repository import log_auth_event
from ..services import auth_mfa_service as mfa
from .auth_login_handler import lock_message


class MfaCodeRequest(BaseModel):
    code: str = Field(min_length=6, max_length=20)


class PasswordConfirmRequest(BaseModel):
    password: str = Field(min_length=1, max_length=128)


class MfaDisableRequest(BaseModel):
    password: str = Field(min_length=1, max_length=128)
    code: str = Field(min_length=6, max_length=20)


def ids(request: Request) -> tuple[UUID, UUID]:
    return UUID(request.state.user["sub"]), UUID(request.state.user["sid"])


async def _run(action, ok_status: int = 200):
    try:
        return await action()
    except mfa.MfaError as err:
        return error(400, str(err), err)
    except mfa.ReauthLockedError as err:
        return error(429, lock_message(err.locked_until), err)
    except AccessDeniedError as err:
        return error(403, str(err), err)
    except Exception as err:
        return error(500, "Error en la verificacion en dos pasos", err)


async def mfa_status_handler(request: Request):
    async def action():
        user = await userService.get_by_id(ids(request)[0])
        return success(200, "Estado de la verificacion en dos pasos", await mfa.status(user))
    return await _run(action)


async def mfa_setup_handler(request: Request, body: PasswordConfirmRequest):
    async def action():
        user = await userService.get_by_id(ids(request)[0])
        data = await mfa.setup(user, body.password)
        return success(200, "Agrega la clave en tu app autenticadora y confirma con un codigo", data)
    return await _run(action)


async def mfa_enable_handler(request: Request, body: MfaCodeRequest):
    async def action():
        user_id, session_id = ids(request)
        codes = await mfa.enable(user_id, session_id, body.code)
        return success(
            200,
            "Verificacion en dos pasos activada. Guarda los codigos de respaldo: no se volveran a mostrar",
            {"recovery_codes": codes},
        )
    return await _run(action)


async def mfa_disable_handler(request: Request, body: MfaDisableRequest):
    async def action():
        user_id, session_id = ids(request)
        user = await userService.get_by_id(user_id)
        await mfa.disable(user, session_id, body.password, body.code)
        return success(200, "Verificacion en dos pasos desactivada")
    return await _run(action)


async def my_sessions_handler(request: Request):
    async def action():
        user_id, session_id = ids(request)
        rows = await sessionRepository.list_active_of_user(user_id)
        data = [
            {**{k: (v.isoformat() if hasattr(v, "isoformat") else str(v) if k == "id" else v) for k, v in row.items()},
             "current": row["id"] == session_id}
            for row in rows
        ]
        return success(200, "Tus sesiones activas", data)
    return await _run(action)


async def revoke_my_session_handler(request: Request, session_id: UUID, body: PasswordConfirmRequest):
    async def action():
        user_id, _ = ids(request)
        await mfa.confirm_password(await userService.get_by_id(user_id), body.password)
        if not await sessionRepository.revoke_own(user_id, session_id):
            return error(404, "Sesion no encontrada o ya cerrada")
        await log_auth_event("SESSION_REVOKED", user_id, "successful", {"session_id": str(session_id)})
        return success(200, "Sesion cerrada")
    return await _run(action)


async def revoke_my_other_sessions_handler(request: Request, body: PasswordConfirmRequest):
    async def action():
        user_id, session_id = ids(request)
        await mfa.confirm_password(await userService.get_by_id(user_id), body.password)
        closed = await sessionRepository.revoke_all_of_user(user_id, "revoked_by_user", session_id)
        await log_auth_event("SESSION_REVOKED", user_id, "successful", {"scope": "others", "closed_sessions": closed})
        return success(200, "Se cerraron tus demas sesiones")
    return await _run(action)


async def reset_user_mfa_handler(request: Request, user_id: str):
    async def action():
        await mfa.reset(ids(request)[0], UUID(user_id))
        return success(200, "Verificacion en dos pasos restablecida: el usuario debera configurarla de nuevo")
    try:
        UUID(user_id)
    except ValueError as err:
        return error(400, "user_id invalido", err)
    return await _run(action)
