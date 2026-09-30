from uuid import UUID

from ....core.db.connection import get_connection
from ...guardian.domain.guardian_domain import Guardian


async def get_guardian_by_user(user_id: UUID) -> Guardian | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            SELECT id, full_name, dni, phone, email, user_id, active, created_at, updated_at
            FROM guardians
            WHERE user_id = $1 AND active = true
            """,
            user_id,
        )

        return Guardian.from_row(row) if row else None

    finally:
        await conn.close()
