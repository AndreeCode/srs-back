from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.child_controls_service import childControlService


async def get_child_control_by_id_handler(child_control_id: str):
    try:
        child_control_uuid = parse_uuid(child_control_id, "child_control_id")
        child_control = await childControlService.get_by_id(child_control_uuid)

        if child_control is None:
            return error(404, "Control no encontrado", ValueError(f"child_control_id={child_control_id}"))

        return success(200, "Control obtenido correctamente", child_control.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener el control", err)
