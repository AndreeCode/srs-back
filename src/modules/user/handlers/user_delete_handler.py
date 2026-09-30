from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.users_service import userService


async def delete_user_handler(user_id: str):
    try:
        user_uuid = parse_uuid(user_id, "user_id")
        result = await userService.delete(user_uuid)

        if result == "not_found":
            return error(404, "Usuario no encontrado", ValueError(f"user_id={user_id}"))

        return success(200, "Usuario desactivado correctamente")

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al eliminar el usuario", err)
