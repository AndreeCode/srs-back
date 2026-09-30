from ....core.db.connection import get_connection
from ..domain.session_domain import Session


async def create_session(session: Session) -> Session:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            INSERT INTO sessions (id, user_id, device_id, token_hash, ip_address, expires_at)
            VALUES ($1, $2, $3, $4, $5::inet, $6)
            RETURNING id, user_id, device_id, token_hash, ip_address, created_at,
                      expires_at, revoked, revoked_reason
            """,
            session.id,
            session.user_id,
            session.device_id,
            session.token_hash,
            session.ip_address,
            session.expires_at,
        )

        return Session.from_row(row)

    finally:
        await conn.close()
