from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.audit_log_domain import AuditLog


async def get_audit_log_by_id(audit_log_id: UUID) -> AuditLog | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            SELECT id, user_id, device_id, action, affected_table, record_id, record_key,
                   ip_address, user_agent, result, details, created_at
            FROM audit_log
            WHERE id = $1
            """,
            audit_log_id,
        )

        if row is None:
            return None

        return AuditLog.from_row(row)

    finally:
        await conn.close()
