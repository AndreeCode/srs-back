from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.users_service import userService


async def get_user_by_id_handler(user_id: str):
    try:
        user_uuid = parse_uuid(user_id, "user_id")
        user = await userService.get_by_id(user_uuid)

        if user is None:
            return error(404, "Usuario no encontrado", ValueError(f"user_id={user_id}"))

        return success(200, "Usuario obtenido correctamente", user.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener el usuario", err)
