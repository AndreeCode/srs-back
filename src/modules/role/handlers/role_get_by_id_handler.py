from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.roles_service import roleService


async def get_role_by_id_handler(role_id: str):
    try:
        role_uuid = parse_uuid(role_id, "role_id")
        role = await roleService.get_by_id(role_uuid)

        if role is None:
            return error(404, "Rol no encontrado", ValueError(f"role_id={role_id}"))

        return success(200, "Rol obtenido correctamente", role.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener el rol", err)
