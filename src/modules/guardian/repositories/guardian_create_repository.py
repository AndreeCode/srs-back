from ....core.db.connection import get_connection
from ..domain.guardian_domain import Guardian


async def create_guardian(guardian: Guardian) -> Guardian:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            INSERT INTO guardians (id, full_name, dni, phone, email, user_id, active)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING id, full_name, dni, phone, email, user_id, active,
                      created_at, updated_at
            """,
            guardian.id,
            guardian.full_name,
            guardian.dni,
            guardian.phone,
            guardian.email,
            guardian.user_id,
            guardian.active,
        )

        return Guardian.from_row(row)

    finally:
        await conn.close()
