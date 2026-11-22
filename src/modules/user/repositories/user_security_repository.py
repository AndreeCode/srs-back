from uuid import UUID

from ....core.db.connection import get_connection


async def _execute(sql: str, *args) -> str:
    conn = await get_connection()
    try:
        return await conn.execute(sql, *args)
    finally:
        await conn.close()


async def get_user_security(user_id: UUID) -> dict | None:
    conn = await get_connection()
    try:
        row = await conn.fetchrow(
            """
            SELECT must_change_password, password_changed_at, mfa_enabled, mfa_secret, mfa_pending_secret,
                   mfa_last_step, mfa_recovery_codes, mfa_enabled_at
            FROM users WHERE id = $1
            """,
            user_id,
        )
        return dict(row) if row else None
    finally:
        await conn.close()


async def mark_password_temporary(user_id: UUID) -> None:
    await _execute("UPDATE users SET must_change_password = TRUE, password_changed_at = NOW() WHERE id = $1", user_id)


async def set_mfa_pending(user_id: UUID, sealed_secret: str) -> None:
    await _execute("UPDATE users SET mfa_pending_secret = $2 WHERE id = $1", user_id, sealed_secret)


async def enable_mfa(user_id: UUID, sealed_secret: str, step: int, recovery: list[str]) -> None:
    await _execute(
        """
        UPDATE users SET mfa_enabled = TRUE, mfa_secret = $2, mfa_pending_secret = NULL, mfa_last_step = $3,
               mfa_recovery_codes = $4, mfa_enabled_at = NOW()
        WHERE id = $1
        """,
        user_id,
        sealed_secret,
        step,
        recovery,
    )


async def clear_mfa(user_id: UUID) -> None:
    await _execute(
        """
        UPDATE users SET mfa_enabled = FALSE, mfa_secret = NULL, mfa_pending_secret = NULL, mfa_last_step = NULL,
               mfa_recovery_codes = '{}', mfa_enabled_at = NULL
        WHERE id = $1
        """,
        user_id,
    )


async def set_mfa_step(user_id: UUID, step: int) -> bool:
    result = await _execute(
        "UPDATE users SET mfa_last_step = $2 WHERE id = $1 AND (mfa_last_step IS NULL OR mfa_last_step < $2)",
        user_id,
        step,
    )
    return result.endswith(" 1")


async def consume_recovery_code(user_id: UUID, code_hash: str) -> bool:
    result = await _execute(
        "UPDATE users SET mfa_recovery_codes = array_remove(mfa_recovery_codes, $2) WHERE id = $1 AND $2 = ANY(mfa_recovery_codes)",
        user_id,
        code_hash,
    )
    return result.endswith(" 1")
