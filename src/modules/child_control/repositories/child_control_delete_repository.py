from uuid import UUID

from ....core.db.connection import get_connection


async def delete_child_control(child_control_id: UUID) -> str:
    conn = await get_connection()

    try:
        result = await conn.execute("DELETE FROM child_controls WHERE id = $1", child_control_id)
        return "not_found" if result.endswith(" 0") else "deleted"

    finally:
        await conn.close()
