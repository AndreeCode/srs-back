from .audit_log_get_all_repository import get_all_audit_logs
from .audit_log_get_by_id_repository import get_audit_log_by_id


class AuditLogRepository:
    get_all = staticmethod(get_all_audit_logs)
    get_by_id = staticmethod(get_audit_log_by_id)


auditLogRepository = AuditLogRepository()
