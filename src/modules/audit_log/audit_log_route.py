from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query

from ...core.security.permission_guard import require_permission
from .domain.audit_log_domain import AuditAction
from .handlers.audit_log_handlers import auditLogHandler

router = APIRouter(prefix="/audit-logs", tags=["audit-logs"])


@router.get("", dependencies=[Depends(require_permission("audit_log.get"))])
async def get_all_audit_logs(
    user_id: str | None = None,
    affected_table: str | None = None,
    record_id: str | None = None,
    action: Optional[AuditAction] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
):
    return await auditLogHandler.get_all(user_id, affected_table, record_id, action, date_from, date_to, limit, offset)


@router.get("/{audit_log_id}", dependencies=[Depends(require_permission("audit_log.get"))])
async def get_audit_log_by_id(audit_log_id: str):
    return await auditLogHandler.get_by_id(audit_log_id)
