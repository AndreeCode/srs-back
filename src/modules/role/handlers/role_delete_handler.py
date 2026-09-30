from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.roles_service import roleService


async def delete_role_handler(role_id: str):
    try:
        role_uuid = parse_uuid(role_id, "role_id")
        result = await roleService.delete(role_uuid)

        if result == "not_found":
            return error(404, "Rol no encontrado", ValueError(f"role_id={role_id}"))

        if result == "deleted":
            return success(200, "Rol eliminado correctamente")

        return success(200, "Rol desactivado porque tiene usuarios asignados")

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al eliminar el rol", err)
