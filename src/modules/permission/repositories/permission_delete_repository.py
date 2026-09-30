from uuid import UUID

from ....core.db.connection import get_connection


async def delete_permission(permission_id: UUID) -> str:
    conn = await get_connection()

    try:
        result = await conn.execute("DELETE FROM permissions WHERE id = $1", permission_id)
        return "not_found" if result.endswith(" 0") else "deleted"

    finally:
        await conn.close()
