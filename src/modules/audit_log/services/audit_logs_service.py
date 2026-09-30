from .audit_log_get_all_service import get_all
from .audit_log_get_by_id_service import get_by_id


class AuditLogService:
    get_all = staticmethod(get_all)
    get_by_id = staticmethod(get_by_id)


auditLogService = AuditLogService()
