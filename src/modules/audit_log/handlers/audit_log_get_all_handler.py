from datetime import date
from typing import Optional

from ....core.http.error import error
from ....core.http.list import list_response
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..domain.audit_log_domain import AuditAction
from ..domain.audit_log_filters import AuditLogFilters
from ..services.audit_logs_service import auditLogService


async def get_all_audit_logs_handler(
    user_id: str | None,
    affected_table: str | None,
    record_id: str | None,
    action: Optional[AuditAction],
    date_from: Optional[date],
    date_to: Optional[date],
    limit: int,
    offset: int,
):
    try:
        filters = AuditLogFilters(
            user_id=parse_uuid(user_id, "user_id") if user_id is not None else None,
            affected_table=affected_table,
            record_id=parse_uuid(record_id, "record_id") if record_id is not None else None,
            action=action,
            date_from=date_from,
            date_to=date_to,
            limit=limit,
            offset=offset,
        )

        audit_logs, total = await auditLogService.get_all(filters)
        data = [audit_log.to_dict() for audit_log in audit_logs]
        meta = {"count": len(data), "total": total, "limit": limit, "offset": offset}
        return list_response(200, "Auditoria obtenida correctamente", data, meta)

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener la auditoria", err)
