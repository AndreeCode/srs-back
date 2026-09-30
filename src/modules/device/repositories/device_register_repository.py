from uuid import UUID, uuid4

from ....core.db.connection import get_connection
from ..domain.device_domain import Device

COLUMNS = """id, user_id, device_hash, user_agent, first_seen_at, last_seen_at, trusted,
             block_scope, blocked_reason, blocked_at, blocked_by"""


async def register_device(user_id: UUID, device_hash: str, user_agent: str | None) -> Device:
    conn = await get_connection()

    try:
        async with conn.transaction():
            row = await conn.fetchrow(
                f"""
                INSERT INTO devices (id, user_id, device_hash, user_agent)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (user_id, device_hash)
                DO UPDATE SET last_seen_at = NOW(), user_agent = EXCLUDED.user_agent
                RETURNING {COLUMNS}
                """,
                uuid4(),
                user_id,
                device_hash,
                user_agent,
            )

            browser_block = await conn.fetchrow(
                """
                SELECT blocked_reason FROM devices
                WHERE device_hash = $1 AND block_scope = 'browser' AND NOT trusted AND id <> $2
                LIMIT 1
                """,
                device_hash,
                row["id"],
            )

            if row["trusted"] and browser_block is not None:
                row = await conn.fetchrow(
                    f"""
                    UPDATE devices SET trusted = false, block_scope = 'browser', blocked_reason = $2
                    WHERE id = $1
                    RETURNING {COLUMNS}
                    """,
                    row["id"],
                    browser_block["blocked_reason"],
                )

        return Device.from_row(row)

    finally:
        await conn.close()
