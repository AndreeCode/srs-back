from ....core.db.connection import get_connection
from ..domain.child_domain import Child


async def create_child(child: Child) -> Child:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            INSERT INTO children (
                id, padron_code, medical_record_code, dni,
                first_names, last_names, birth_date, gender, birth_condition,
                mother_name, mother_dni, address, contact_phone, insurance,
                health_facility_id, active, registered_by
            )
            VALUES (
                $1, $2, $3, $4,
                $5, $6, $7, $8, $9,
                $10, $11, $12, $13, $14,
                $15, $16, $17
            )
            RETURNING id, padron_code, medical_record_code, dni,
                      first_names, last_names, birth_date, gender, birth_condition,
                      mother_name, mother_dni, address, contact_phone, insurance,
                      health_facility_id, active, registered_by,
                      created_at, updated_at
            """,
            child.id,
            child.padron_code,
            child.medical_record_code,
            child.dni,
            child.first_names,
            child.last_names,
            child.birth_date,
            child.gender,
            child.birth_condition,
            child.mother_name,
            child.mother_dni,
            child.address,
            child.contact_phone,
            child.insurance,
            child.health_facility_id,
            child.active,
            child.registered_by,
        )

        return Child.from_row(row)

    finally:
        await conn.close()
