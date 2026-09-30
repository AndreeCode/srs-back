from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.session_domain import Session


async def get_session_by_id(session_id: UUID) -> Session | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            SELECT id, user_id, device_id, token_hash, ip_address, created_at,
                   expires_at, revoked, revoked_reason
            FROM sessions
            WHERE id = $1
            """,
            session_id,
        )

        if row is None:
            return None

        return Session.from_row(row)

    finally:
        await conn.close()
