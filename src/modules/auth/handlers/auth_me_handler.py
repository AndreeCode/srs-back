from uuid import UUID

from fastapi import Request

from ....core.http.error import error
from ....core.http.succes import success
from ...role.services.roles_service import roleService
from ...user.repositories.user_repositories import userRepository
from ...user.services.users_service import userService
from ..services import auth_mfa_service as mfa


async def get_me_handler(request: Request):
    payload = request.state.user

    try:
        user = await userService.get_by_id(UUID(payload["sub"]))

        if user is None:
            return error(404, "Usuario no encontrado", ValueError(f"user_id={payload['sub']}"))

        role = await roleService.get_by_id(user.role_id)
        security = await userRepository.security(user.id)
        expires = mfa.temp_password_expires_at(security)
        required = mfa.required_for(role.name if role else None)
        return success(
            200,
            "Usuario autenticado",
            {
                **user.to_dict(),
                "role": role.name if role else None,
                "must_change_password": bool(security["must_change_password"]),
                "temp_password_expires_at": expires.isoformat() if expires else None,
                "mfa_enabled": bool(security["mfa_enabled"]),
                "mfa_required": required,
                "mfa_setup_required": required and not security["mfa_enabled"],
            },
        )

    except Exception as err:
        return error(500, "Error al obtener el usuario autenticado", err)
