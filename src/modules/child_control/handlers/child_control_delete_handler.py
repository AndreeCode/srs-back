from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.child_controls_service import childControlService


async def delete_child_control_handler(child_control_id: str):
    try:
        child_control_uuid = parse_uuid(child_control_id, "child_control_id")
        result = await childControlService.delete(child_control_uuid)

        if result == "not_found":
            return error(404, "Control no encontrado", ValueError(f"child_control_id={child_control_id}"))

        return success(200, "Control eliminado correctamente")

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al eliminar el control", err)
