from ..domain.audit_log_domain import AuditLog
from ..domain.audit_log_filters import AuditLogFilters
from ..repositories.audit_log_repositories import auditLogRepository


async def get_all(filters: AuditLogFilters) -> tuple[list[AuditLog], int]:
    return await auditLogRepository.get_all(filters)
