from uuid import UUID

from ....core.db.connection import get_connection


async def user_has_permission(user_id: UUID, code: str) -> bool:
    conn = await get_connection()

    try:
        return await conn.fetchval(
            """
            SELECT EXISTS (
                SELECT 1
                FROM users u
                JOIN roles r ON r.id = u.role_id
                JOIN role_permission rp ON rp.role_id = r.id
                JOIN permissions p ON p.id = rp.permission_id
                WHERE u.id = $1
                  AND u.active AND NOT u.blocked
                  AND r.is_active
                  AND p.code = $2
            )
            """,
            user_id,
            code,
        )

    finally:
        await conn.close()
