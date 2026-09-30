from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.device_domain import Device


async def get_device_by_id(device_id: UUID) -> Device | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            SELECT id, user_id, device_hash, user_agent, first_seen_at, last_seen_at, trusted,
                   block_scope, blocked_reason, blocked_at, blocked_by
            FROM devices
            WHERE id = $1
            """,
            device_id,
        )

        if row is None:
            return None

        return Device.from_row(row)

    finally:
        await conn.close()
