from ....core.http.error import error
from ....core.http.list import list_response
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.devices_service import deviceService


async def get_all_devices_handler(user_id: str | None):
    try:
        user_uuid = parse_uuid(user_id, "user_id") if user_id is not None else None

        devices = await deviceService.get_all(user_uuid)
        data = [device.to_dict() for device in devices]
        return list_response(200, "Dispositivos obtenidos correctamente", data, {"count": len(data)})

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener los dispositivos", err)
