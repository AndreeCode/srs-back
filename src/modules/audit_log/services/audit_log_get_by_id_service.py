from uuid import UUID

from ..domain.audit_log_domain import AuditLog
from ..repositories.audit_log_repositories import auditLogRepository


async def get_by_id(audit_log_id: UUID) -> AuditLog | None:
    return await auditLogRepository.get_by_id(audit_log_id)
