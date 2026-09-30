from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.permissions_service import permissionService


async def delete_permission_handler(permission_id: str):
    try:
        permission_uuid = parse_uuid(permission_id, "permission_id")
        result = await permissionService.delete(permission_uuid)

        if result == "not_found":
            return error(404, "Permiso no encontrado", ValueError(f"permission_id={permission_id}"))

        return success(200, "Permiso eliminado correctamente")

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al eliminar el permiso", err)
