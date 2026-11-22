from datetime import datetime
from uuid import UUID

from ....core.db.connection import get_connection


async def get_user_locked_until(user_id: UUID) -> datetime | None:
    conn = await get_connection()

    try:
        return await conn.fetchval("SELECT locked_until FROM users WHERE id = $1 AND locked_until > NOW()", user_id)

    finally:
        await conn.close()


async def register_user_login_failure(user_id: UUID, max_attempts: int, lock_seconds: float) -> datetime | None:
    conn = await get_connection()

    try:
        return await conn.fetchval(
            """
            WITH n AS (
                SELECT CASE WHEN locked_until IS NOT NULL AND locked_until <= NOW() THEN 1
                            ELSE failed_attempts + 1 END AS attempts
                FROM users WHERE id = $1
            )
            UPDATE users SET
                failed_attempts = CASE WHEN n.attempts >= $2 THEN 0 ELSE n.attempts END,
                locked_until = CASE WHEN n.attempts >= $2 THEN NOW() + make_interval(secs => $3) ELSE NULL END
            FROM n
            WHERE users.id = $1
            RETURNING users.locked_until
            """,
            user_id,
            max_attempts,
            lock_seconds,
        )

    finally:
        await conn.close()


async def reset_user_login_failures(user_id: UUID) -> None:
    conn = await get_connection()

    try:
        await conn.execute(
            "UPDATE users SET failed_attempts = 0, locked_until = NULL WHERE id = $1 AND (failed_attempts <> 0 OR locked_until IS NOT NULL)",
            user_id,
        )

    finally:
        await conn.close()


async def set_user_password(user_id: UUID, password_hash: str) -> None:
    conn = await get_connection()

    try:
        await conn.execute(
            "UPDATE users SET password_hash = $2, password_changed_at = NOW(), must_change_password = FALSE, failed_attempts = 0, locked_until = NULL WHERE id = $1",
            user_id,
            password_hash,
        )

    finally:
        await conn.close()
