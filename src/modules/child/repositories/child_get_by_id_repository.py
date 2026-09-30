from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.child_domain import Child


async def get_child_by_id(child_id: UUID) -> Child | None:
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
            WHERE id = $1
            """,
            child_id,
        )

        if row is None:
            return None

        return Child.from_row(row)

    finally:
        await conn.close()
