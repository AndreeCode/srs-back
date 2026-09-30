from typing import Optional

from pydantic import BaseModel, Field

from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..domain.device_domain import BlockScope
from ..services.devices_service import deviceService


class DeviceUpdateRequest(BaseModel):
    trusted: bool
    blocked_reason: Optional[str] = Field(default=None, max_length=500)
    scope: BlockScope = "account"


async def update_device_handler(device_id: str, body: DeviceUpdateRequest):
    try:
        device_uuid = parse_uuid(device_id, "device_id")

        if not body.trusted and not (body.blocked_reason or "").strip():
            return error(400, "Indica el motivo del bloqueo", ValueError("blocked_reason required"))

        updated = await deviceService.update(device_uuid, body.trusted, (body.blocked_reason or "").strip() or None, body.scope)

        if updated is None:
            return error(404, "Dispositivo no encontrado", ValueError(f"device_id={device_id}"))

        if body.trusted:
            msg = "Navegador desbloqueado para todas las cuentas" if body.scope == "browser" else "Dispositivo desbloqueado"
        else:
            msg = (
                "Navegador bloqueado para todas las cuentas y sus sesiones cerradas"
                if body.scope == "browser"
                else "Dispositivo bloqueado y sus sesiones cerradas"
            )
        return success(200, msg, updated.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al actualizar el dispositivo", err)
