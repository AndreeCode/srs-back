from uuid import UUID

from ....core.db.connection import get_connection


async def delete_child_guardian(child_id: UUID, guardian_id: UUID) -> str:
    conn = await get_connection()

    try:
        result = await conn.execute(
            "DELETE FROM child_guardian WHERE child_id = $1 AND guardian_id = $2",
            child_id,
            guardian_id,
        )
        return "not_found" if result.endswith(" 0") else "deleted"

    finally:
        await conn.close()
