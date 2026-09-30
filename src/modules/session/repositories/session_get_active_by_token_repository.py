from ....core.db.connection import get_connection
from ..domain.session_domain import Session


async def get_active_session_by_token(token_hash: str) -> Session | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            SELECT s.id, s.user_id, s.device_id, s.token_hash, s.ip_address, s.created_at,
                   s.expires_at, s.revoked, s.revoked_reason
            FROM sessions s
            JOIN devices d ON d.id = s.device_id
            WHERE s.token_hash = $1
              AND NOT s.revoked
              AND s.expires_at > NOW()
              AND d.trusted
            """,
            token_hash,
        )

        if row is None:
            return None

        return Session.from_row(row)

    finally:
        await conn.close()
