from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.device_domain import BlockScope, Device

COLUMNS = """id, user_id, device_hash, user_agent, first_seen_at, last_seen_at, trusted,
             block_scope, blocked_reason, blocked_at, blocked_by"""


async def update_device(device_id: UUID, trusted: bool, reason: str | None, scope: BlockScope) -> Device | None:
    conn = await get_connection()

    try:
        async with conn.transaction():
            device_hash = await conn.fetchval("SELECT device_hash FROM devices WHERE id = $1", device_id)

            if device_hash is None:
                return None

            if scope == "browser":
                targets = await conn.fetch("SELECT id FROM devices WHERE device_hash = $1", device_hash)
                target_ids = [row["id"] for row in targets]
            else:
                target_ids = [device_id]

            if trusted:
                await conn.execute("UPDATE devices SET trusted = true WHERE id = ANY($1::uuid[])", target_ids)
            else:
                await conn.execute(
                    """
                    UPDATE devices SET trusted = false, block_scope = $1, blocked_reason = $2
                    WHERE id = ANY($3::uuid[])
                    """,
                    scope,
                    reason,
                    target_ids,
                )
                await conn.execute(
                    """
                    UPDATE sessions SET revoked = true, revoked_reason = 'device_blocked'
                    WHERE NOT revoked AND device_id = ANY($1::uuid[])
                    """,
                    target_ids,
                )

            row = await conn.fetchrow(f"SELECT {COLUMNS} FROM devices WHERE id = $1", device_id)

        return Device.from_row(row)

    finally:
        await conn.close()
