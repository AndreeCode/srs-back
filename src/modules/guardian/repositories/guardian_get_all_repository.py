from ....core.db.connection import get_connection
from ..domain.guardian_domain import Guardian


async def get_all_guardians() -> list[Guardian]:
    conn = await get_connection()

    try:
        rows = await conn.fetch(
            """
            SELECT id, full_name, dni, phone, email, user_id, active,
                   created_at, updated_at
            FROM guardians
            WHERE active = true
            ORDER BY full_name
            """
        )

        return [Guardian.from_row(row) for row in rows]

    finally:
        await conn.close()
