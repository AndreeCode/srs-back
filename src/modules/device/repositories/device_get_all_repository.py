from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.device_domain import Device


async def get_all_devices(user_id: UUID | None) -> list[Device]:
    conn = await get_connection()

    try:
        rows = await conn.fetch(
            """
            SELECT id, user_id, device_hash, user_agent, first_seen_at, last_seen_at, trusted,
                   block_scope, blocked_reason, blocked_at, blocked_by
            FROM devices
            WHERE ($1::uuid IS NULL OR user_id = $1)
            ORDER BY last_seen_at DESC
            """,
            user_id,
        )

        return [Device.from_row(row) for row in rows]

    finally:
        await conn.close()
