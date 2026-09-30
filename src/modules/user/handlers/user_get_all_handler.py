from ....core.http.error import error
from ....core.http.list import list_response
from ..services.users_service import userService


async def get_all_users_handler():
    try:
        users = await userService.get_all()
        data = [user.to_dict() for user in users]
        return list_response(200, "Usuarios obtenidos correctamente", data, {"count": len(data)})

    except Exception as err:
        return error(500, "Error al obtener los usuarios", err)
