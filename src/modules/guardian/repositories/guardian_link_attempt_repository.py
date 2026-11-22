from uuid import UUID

from ....core.db.connection import get_connection


async def count_link_failures(identifier_hash: str, ip: str | None, user_id: UUID | None) -> dict[str, int]:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            SELECT
                count(*) FILTER (WHERE identifier_hash = $1 AND created_at > NOW() - INTERVAL '24 hours') AS identifier,
                count(*) FILTER (WHERE $2::text IS NOT NULL AND ip_address = $2::text::inet
                                   AND created_at > NOW() - INTERVAL '1 hour') AS ip,
                count(*) FILTER (WHERE $3::uuid IS NOT NULL AND user_id = $3
                                   AND created_at > NOW() - INTERVAL '24 hours') AS account
            FROM portal_link_attempts
            WHERE NOT success AND created_at > NOW() - INTERVAL '24 hours'
            """,
            identifier_hash,
            ip,
            user_id,
        )
        return dict(row)

    finally:
        await conn.close()


async def record_link_attempt(identifier_hash: str, ip: str | None, user_id: UUID | None, success: bool) -> None:
    conn = await get_connection()

    try:
        await conn.execute(
            "INSERT INTO portal_link_attempts (identifier_hash, ip_address, user_id, success) VALUES ($1, $2::text::inet, $3, $4)",
            identifier_hash,
            ip,
            user_id,
            success,
        )
        await conn.execute("DELETE FROM portal_link_attempts WHERE created_at < NOW() - INTERVAL '7 days'")

    finally:
        await conn.close()
