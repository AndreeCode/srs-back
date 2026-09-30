from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.devices_service import deviceService


async def get_device_by_id_handler(device_id: str):
    try:
        device_uuid = parse_uuid(device_id, "device_id")
        device = await deviceService.get_by_id(device_uuid)

        if device is None:
            return error(404, "Dispositivo no encontrado", ValueError(f"device_id={device_id}"))

        return success(200, "Dispositivo obtenido correctamente", device.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener el dispositivo", err)
