from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.session_domain import Session


async def get_all_sessions(user_id: UUID | None, device_id: UUID | None, active: bool | None) -> list[Session]:
    conn = await get_connection()

    try:
        rows = await conn.fetch(
            """
            SELECT id, user_id, device_id, token_hash, ip_address, created_at,
                   expires_at, revoked, revoked_reason
            FROM sessions
            WHERE ($1::uuid IS NULL OR user_id = $1)
              AND ($2::uuid IS NULL OR device_id = $2)
              AND ($3::boolean IS NULL OR (NOT revoked AND expires_at > NOW()) = $3)
            ORDER BY created_at DESC
            """,
            user_id,
            device_id,
            active,
        )

        return [Session.from_row(row) for row in rows]

    finally:
        await conn.close()
