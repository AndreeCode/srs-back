from uuid import UUID

from ....core.db.connection import get_connection


async def _execute(sql: str, *args) -> str:
    conn = await get_connection()
    try:
        return await conn.execute(sql, *args)
    finally:
        await conn.close()


async def get_session_access(token_hash: str) -> dict | None:
    conn = await get_connection()
    try:
        row = await conn.fetchrow(
            """
            SELECT s.id, s.user_id, s.device_id, s.last_activity_at, u.must_change_password, u.mfa_enabled,
                   r.name AS role_name
            FROM sessions s
            JOIN devices d ON d.id = s.device_id
            JOIN users u ON u.id = s.user_id
            JOIN roles r ON r.id = u.role_id
            WHERE s.token_hash = $1 AND NOT s.revoked AND s.expires_at > NOW() AND d.trusted
            """,
            token_hash,
        )
        return dict(row) if row else None
    finally:
        await conn.close()


async def touch_session(session_id: UUID) -> None:
    await _execute("UPDATE sessions SET last_activity_at = NOW() WHERE id = $1", session_id)


async def revoke_idle_session(session_id: UUID) -> None:
    await _execute("UPDATE sessions SET revoked = TRUE, revoked_reason = 'idle_timeout' WHERE id = $1 AND NOT revoked", session_id)


async def list_active_sessions_of_user(user_id: UUID) -> list[dict]:
    conn = await get_connection()
    try:
        rows = await conn.fetch(
            """
            SELECT s.id, s.created_at, s.last_activity_at, s.expires_at, host(s.ip_address) AS ip_address, d.user_agent
            FROM sessions s
            JOIN devices d ON d.id = s.device_id
            WHERE s.user_id = $1 AND NOT s.revoked AND s.expires_at > NOW()
            ORDER BY s.last_activity_at DESC
            """,
            user_id,
        )
        return [dict(row) for row in rows]
    finally:
        await conn.close()


async def revoke_own_session(user_id: UUID, session_id: UUID) -> bool:
    result = await _execute(
        "UPDATE sessions SET revoked = TRUE, revoked_reason = 'revoked_by_user' WHERE id = $1 AND user_id = $2 AND NOT revoked",
        session_id,
        user_id,
    )
    return result.endswith(" 1")
