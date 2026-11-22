from datetime import date

from ....core.db.connection import get_connection
from ..domain.child_domain import Child


async def find_child_by_identifier(identifier: str, birth_date: date) -> Child | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            SELECT id, padron_code, medical_record_code, dni,
                   first_names, last_names, birth_date, gender, birth_condition,
                   mother_name, mother_dni, address, contact_phone, insurance,
                   health_facility_id, active, registered_by,
                   created_at, updated_at
            FROM children
            WHERE (dni = $1 OR padron_code = $1) AND birth_date = $2 AND active = true
            LIMIT 1
            """,
            identifier,
            birth_date,
        )

        return Child.from_row(row) if row else None

    finally:
        await conn.close()
