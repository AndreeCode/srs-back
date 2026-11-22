from ....core.db.connection import get_connection
from ..domain.guardian_domain import Guardian


async def get_guardian_by_dni(dni: str) -> Guardian | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            SELECT id, full_name, dni, phone, email, user_id, active, created_at, updated_at
            FROM guardians
            WHERE dni = $1
            """,
            dni,
        )

        return Guardian.from_row(row) if row else None

    finally:
        await conn.close()
