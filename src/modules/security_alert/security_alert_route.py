from fastapi import APIRouter, Depends, Request

from ...core.security.permission_guard import require_permission
from .handlers.security_alert_handlers import SecurityAlertUpdateRequest, securityAlertHandler

router = APIRouter(prefix="/security-alerts", tags=["security-alerts"])


@router.get("", dependencies=[Depends(require_permission("security_alert.get"))])
async def get_all_security_alerts(status: str | None = None):
    return await securityAlertHandler.get_all(status)


@router.post("/scan", dependencies=[Depends(require_permission("security_alert.post"))])
async def scan_security_alerts():
    return await securityAlertHandler.scan()


@router.put("/{alert_id}", dependencies=[Depends(require_permission("security_alert.put"))])
async def update_security_alert(request: Request, alert_id: str, body: SecurityAlertUpdateRequest):
    return await securityAlertHandler.update(request, alert_id, body)
