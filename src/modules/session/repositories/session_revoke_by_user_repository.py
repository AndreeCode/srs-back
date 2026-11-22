from uuid import UUID

from ....core.db.connection import get_connection


async def revoke_sessions_of_user(user_id: UUID, reason: str, keep_session_id: UUID | None = None) -> int:
    conn = await get_connection()

    try:
        result = await conn.execute(
            """
            UPDATE sessions SET revoked = true, revoked_reason = $2
            WHERE user_id = $1 AND NOT revoked AND ($3::uuid IS NULL OR id <> $3)
            """,
            user_id,
            reason,
            keep_session_id,
        )
        return int(result.split()[-1])

    finally:
        await conn.close()
