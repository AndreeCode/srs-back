from ....core.http.error import error
from ....core.http.list import list_response
from ..services.roles_service import roleService


async def get_all_roles_handler():
    try:
        roles = await roleService.get_all()
        data = [role.to_dict() for role in roles]
        return list_response(200, "Roles obtenidos correctamente", data, {"count": len(data)})

    except Exception as err:
        return error(500, "Error al obtener los roles", err)
