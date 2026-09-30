from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.permissions_service import permissionService


async def get_permission_by_id_handler(permission_id: str):
    try:
        permission_uuid = parse_uuid(permission_id, "permission_id")
        permission = await permissionService.get_by_id(permission_uuid)

        if permission is None:
            return error(404, "Permiso no encontrado", ValueError(f"permission_id={permission_id}"))

        return success(200, "Permiso obtenido correctamente", permission.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener el permiso", err)
