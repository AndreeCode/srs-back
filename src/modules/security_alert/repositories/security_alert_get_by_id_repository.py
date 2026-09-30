from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.security_alert_domain import SecurityAlert
from .security_alert_columns import COLUMNS


async def get_security_alert_by_id(alert_id: UUID) -> SecurityAlert | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(f"SELECT {COLUMNS} FROM security_alerts WHERE id = $1", alert_id)
        return SecurityAlert.from_row(row) if row else None

    finally:
        await conn.close()
