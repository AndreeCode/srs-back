from ....core.db.connection import get_connection
from ..domain.audit_log_domain import AuditLog
from ..domain.audit_log_filters import AuditLogFilters


async def get_all_audit_logs(filters: AuditLogFilters) -> tuple[list[AuditLog], int]:
    conn = await get_connection()

    try:
        rows = await conn.fetch(
            """
            SELECT id, user_id, device_id, action, affected_table, record_id, record_key,
                   ip_address, user_agent, result, details, created_at,
                   count(*) OVER () AS total
            FROM audit_log
            WHERE ($1::uuid IS NULL OR user_id = $1)
              AND ($2::text IS NULL OR affected_table = $2)
              AND ($3::uuid IS NULL OR record_id = $3)
              AND ($4::text IS NULL OR action = $4)
              AND ($5::date IS NULL OR created_at >= $5::date)
              AND ($6::date IS NULL OR created_at < $6::date + 1)
            ORDER BY created_at DESC
            LIMIT $7 OFFSET $8
            """,
            filters.user_id,
            filters.affected_table,
            filters.record_id,
            filters.action,
            filters.date_from,
            filters.date_to,
            filters.limit,
            filters.offset,
        )

        total = rows[0]["total"] if rows else 0
        return [AuditLog.from_row(row) for row in rows], total

    finally:
        await conn.close()
