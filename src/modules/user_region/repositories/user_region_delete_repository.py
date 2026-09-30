from uuid import UUID

from ....core.db.connection import get_connection


async def delete_user_region(user_id: UUID, region_id: UUID) -> str:
    conn = await get_connection()

    try:
        result = await conn.execute(
            "DELETE FROM user_region WHERE user_id = $1 AND region_id = $2",
            user_id,
            region_id,
        )
        return "not_found" if result.endswith(" 0") else "deleted"

    finally:
        await conn.close()
