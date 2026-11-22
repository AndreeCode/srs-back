from uuid import UUID

from ....core.db.connection import get_connection


async def get_user_access(user_id: UUID) -> tuple[UUID | None, set[UUID]]:
    conn = await get_connection()

    try:
        role_id = await conn.fetchval("SELECT role_id FROM users WHERE id = $1", user_id)
        rows = await conn.fetch(
            """
            SELECT rp.permission_id
            FROM users u
            JOIN roles r ON r.id = u.role_id
            JOIN role_permission rp ON rp.role_id = r.id
            WHERE u.id = $1
              AND u.active AND NOT u.blocked
              AND r.is_active
            """,
            user_id,
        )
        return role_id, {row["permission_id"] for row in rows}

    finally:
        await conn.close()
