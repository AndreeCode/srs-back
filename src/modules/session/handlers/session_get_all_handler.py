from ....core.http.error import error
from ....core.http.list import list_response
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.sessions_service import sessionService


async def get_all_sessions_handler(user_id: str | None, device_id: str | None, active: bool | None):
    try:
        user_uuid = parse_uuid(user_id, "user_id") if user_id is not None else None
        device_uuid = parse_uuid(device_id, "device_id") if device_id is not None else None

        sessions = await sessionService.get_all(user_uuid, device_uuid, active)
        data = [session.to_dict() for session in sessions]
        return list_response(200, "Sesiones obtenidas correctamente", data, {"count": len(data)})

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener las sesiones", err)
