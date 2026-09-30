from ....core.db.connection import get_connection
from ..domain.child_domain import Child


async def get_all_children() -> list[Child]:
    conn = await get_connection()

    try:
        rows = await conn.fetch(
            """
            SELECT id, padron_code, medical_record_code, dni,
                   first_names, last_names, birth_date, gender, birth_condition,
                   mother_name, mother_dni, address, contact_phone, insurance,
                   health_facility_id, active, registered_by,
                   created_at, updated_at
            FROM children
            WHERE active = true
            ORDER BY last_names, first_names
            """
        )

        return [Child.from_row(row) for row in rows]

    finally:
        await conn.close()
