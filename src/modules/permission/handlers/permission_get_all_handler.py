from ....core.http.error import error
from ....core.http.list import list_response
from ..services.permissions_service import permissionService


async def get_all_permissions_handler():
    try:
        permissions = await permissionService.get_all()
        data = [permission.to_dict() for permission in permissions]
        return list_response(200, "Permisos obtenidos correctamente", data, {"count": len(data)})

    except Exception as err:
        return error(500, "Error al obtener los permisos", err)
