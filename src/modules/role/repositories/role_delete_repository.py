from uuid import UUID

from ....core.db.connection import get_connection


async def delete_role(role_id: UUID) -> str:
    conn = await get_connection()

    try:
        users_count = await conn.fetchval(
            "SELECT COUNT(*) FROM users WHERE role_id = $1",
            role_id,
        )

        if users_count == 0:
            result = await conn.execute("DELETE FROM roles WHERE id = $1", role_id)
            return "not_found" if result.endswith(" 0") else "deleted"

        result = await conn.execute(
            "UPDATE roles SET is_active = false WHERE id = $1",
            role_id,
        )
        return "not_found" if result.endswith(" 0") else "deactivated"

    finally:
        await conn.close()
