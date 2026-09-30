from ....core.db.connection import get_connection


async def revoke_session_by_token(token_hash: str, reason: str) -> None:
    conn = await get_connection()

    try:
        await conn.execute(
            "UPDATE sessions SET revoked = true, revoked_reason = $2 WHERE token_hash = $1 AND NOT revoked",
            token_hash,
            reason,
        )

    finally:
        await conn.close()
