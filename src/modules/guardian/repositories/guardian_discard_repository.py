from uuid import UUID

from ....core.db.connection import get_connection


async def discard_new_guardian(guardian_id: UUID) -> None:
    conn = await get_connection()

    try:
        await conn.execute("DELETE FROM guardians WHERE id = $1 AND user_id IS NULL", guardian_id)

    finally:
        await conn.close()
