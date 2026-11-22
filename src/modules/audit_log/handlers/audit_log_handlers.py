from .audit_log_get_all_handler import get_all_audit_logs_handler
from .audit_log_get_by_id_handler import get_audit_log_by_id_handler
from .audit_log_verify_handler import verify_audit_chain_handler


class AuditLogHandler:
    get_all = staticmethod(get_all_audit_logs_handler)
    get_by_id = staticmethod(get_audit_log_by_id_handler)
    verify = staticmethod(verify_audit_chain_handler)


auditLogHandler = AuditLogHandler()
