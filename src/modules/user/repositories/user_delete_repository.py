from uuid import UUID

from ....core.db.connection import get_connection


async def delete_user(user_id: UUID) -> str:
    conn = await get_connection()

    try:
        result = await conn.execute(
            "UPDATE users SET active = false WHERE id = $1",
            user_id,
        )
        return "not_found" if result.endswith(" 0") else "deactivated"

    finally:
        await conn.close()
