from ....core.db.connection import get_connection
from ..domain.security_alert_domain import SecurityAlert
from .security_alert_columns import COLUMNS


async def get_all_security_alerts(status: str | None) -> list[SecurityAlert]:
    conn = await get_connection()

    try:
        rows = await conn.fetch(
            f"""
            SELECT {COLUMNS} FROM security_alerts
            WHERE ($1::text IS NULL OR status = $1)
            ORDER BY (status = 'open') DESC, updated_at DESC
            LIMIT 200
            """,
            status,
        )

        return [SecurityAlert.from_row(row) for row in rows]

    finally:
        await conn.close()
