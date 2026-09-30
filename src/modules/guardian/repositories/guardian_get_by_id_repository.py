from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.guardian_domain import Guardian


async def get_guardian_by_id(guardian_id: UUID) -> Guardian | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            SELECT id, full_name, dni, phone, email, user_id, active,
                   created_at, updated_at
            FROM guardians
            WHERE id = $1
            """,
            guardian_id,
        )

        if row is None:
            return None

        return Guardian.from_row(row)

    finally:
        await conn.close()
