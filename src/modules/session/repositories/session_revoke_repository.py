from uuid import UUID

from ....core.db.connection import get_connection


async def revoke_session(session_id: UUID, reason: str) -> str:
    conn = await get_connection()

    try:
        result = await conn.execute(
            "UPDATE sessions SET revoked = true, revoked_reason = $2 WHERE id = $1 AND NOT revoked",
            session_id,
            reason,
        )

        if not result.endswith(" 0"):
            return "revoked"

        exists = await conn.fetchval("SELECT EXISTS (SELECT 1 FROM sessions WHERE id = $1)", session_id)
        return "already_revoked" if exists else "not_found"

    finally:
        await conn.close()
