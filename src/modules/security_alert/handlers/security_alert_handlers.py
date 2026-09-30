from typing import Literal, Optional
from uuid import UUID

from fastapi import Request
from pydantic import BaseModel, Field

from ....core.http.error import error
from ....core.http.list import list_response
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.security_alerts_service import securityAlertService


class SecurityAlertUpdateRequest(BaseModel):
    status: Literal["open", "resolved", "dismissed"]
    resolution: Optional[str] = Field(default=None, max_length=1000)


async def get_all_security_alerts_handler(status: str | None):
    try:
        if status is not None and status not in ("open", "resolved", "dismissed"):
            return error(400, "status debe ser open, resolved o dismissed", ValueError(status))

        alerts = await securityAlertService.get_all(status)
        return list_response(200, "Alertas obtenidas correctamente", [a.to_dict() for a in alerts], {"total": len(alerts)})

    except Exception as err:
        return error(500, "Error al obtener las alertas", err)


async def update_security_alert_handler(request: Request, alert_id: str, body: SecurityAlertUpdateRequest):
    try:
        alert_uuid = parse_uuid(alert_id, "alert_id")

        if body.status != "open" and not (body.resolution or "").strip():
            return error(400, "Indica qué se hizo con la alerta", ValueError("resolution required"))

        updated = await securityAlertService.update(
            alert_uuid, body.status, (body.resolution or "").strip() or None, UUID(request.state.user["sub"])
        )

        if updated is None:
            return error(404, "Alerta no encontrada", ValueError(f"alert_id={alert_id}"))

        msg = {"open": "Alerta reabierta", "resolved": "Alerta resuelta", "dismissed": "Alerta descartada"}[body.status]
        return success(200, msg, updated.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al actualizar la alerta", err)


async def scan_security_alerts_handler():
    try:
        created = await securityAlertService.scan()
        msg = f"Revisión terminada: {created} alerta(s) nueva(s)" if created else "Revisión terminada: sin alertas nuevas"
        return success(200, msg, {"created": created})

    except Exception as err:
        return error(500, "Error al revisar la actividad", err)


class SecurityAlertHandler:
    get_all = staticmethod(get_all_security_alerts_handler)
    update = staticmethod(update_security_alert_handler)
    scan = staticmethod(scan_security_alerts_handler)


securityAlertHandler = SecurityAlertHandler()
