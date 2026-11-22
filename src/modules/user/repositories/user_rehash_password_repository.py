from uuid import UUID

from ....core.db.connection import get_connection


async def rehash_user_password(user_id: UUID, password_hash: str) -> None:
    conn = await get_connection()

    try:
        await conn.execute("UPDATE users SET password_hash = $2 WHERE id = $1", user_id, password_hash)

    finally:
        await conn.close()
