from uuid import UUID

from fastapi import Request

from ....core.http.error import error
from ....core.http.succes import success
from ...role.services.roles_service import roleService
from ...user.services.users_service import userService


async def get_me_handler(request: Request):
    payload = request.state.user

    try:
        user = await userService.get_by_id(UUID(payload["sub"]))

        if user is None:
            return error(404, "Usuario no encontrado", ValueError(f"user_id={payload['sub']}"))

        role = await roleService.get_by_id(user.role_id)
        return success(200, "Usuario autenticado", {**user.to_dict(), "role": role.name if role else None})

    except Exception as err:
        return error(500, "Error al obtener el usuario autenticado", err)
