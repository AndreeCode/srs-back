from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.security_alert_domain import SecurityAlert
from .security_alert_columns import COLUMNS


async def update_security_alert(alert_id: UUID, status: str, resolution: str | None, resolved_by: UUID) -> SecurityAlert | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            f"""
            UPDATE security_alerts
            SET status = $2,
                resolution = $3,
                resolved_by = CASE WHEN $2 = 'open' THEN NULL ELSE $4::uuid END,
                resolved_at = CASE WHEN $2 = 'open' THEN NULL ELSE NOW() END
            WHERE id = $1
            RETURNING {COLUMNS}
            """,
            alert_id,
            status,
            resolution,
            resolved_by,
        )

        return SecurityAlert.from_row(row) if row else None

    finally:
        await conn.close()
