from ....core.db.connection import get_connection
from ..domain.guardian_domain import Guardian


async def update_guardian(guardian: Guardian) -> Guardian | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            UPDATE guardians
            SET full_name = $1,
                dni = $2,
                phone = $3,
                email = $4,
                user_id = $5,
                active = $6
            WHERE id = $7
            RETURNING id, full_name, dni, phone, email, user_id, active,
                      created_at, updated_at
            """,
            guardian.full_name,
            guardian.dni,
            guardian.phone,
            guardian.email,
            guardian.user_id,
            guardian.active,
            guardian.id,
        )

        if row is None:
            return None

        return Guardian.from_row(row)

    finally:
        await conn.close()
