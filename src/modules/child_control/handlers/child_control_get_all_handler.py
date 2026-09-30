from typing import Optional

from ....core.http.error import error
from ....core.http.list import list_response
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..domain.child_control_domain import ControlStatus
from ..services.child_controls_service import childControlService


async def get_all_child_controls_handler(
    child_id: str | None,
    service_id: str | None,
    status: Optional[ControlStatus],
):
    try:
        child_uuid = parse_uuid(child_id, "child_id") if child_id is not None else None
        service_uuid = parse_uuid(service_id, "service_id") if service_id is not None else None

        child_controls = await childControlService.get_all(child_uuid, service_uuid, status)
        data = [child_control.to_dict() for child_control in child_controls]
        return list_response(200, "Controles obtenidos correctamente", data, {"count": len(data)})

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener los controles", err)
