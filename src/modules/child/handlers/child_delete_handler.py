from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.children_service import childService


async def delete_child_handler(child_id: str):
    try:
        child_uuid = parse_uuid(child_id, "child_id")
        result = await childService.delete(child_uuid)

        if result == "not_found":
            return error(404, "Nino no encontrado", ValueError(f"child_id={child_id}"))

        return success(200, "Nino desactivado correctamente")

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al eliminar el nino", err)
