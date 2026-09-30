from ....core.db.connection import get_connection
from ..domain.child_domain import Child


async def update_child(child: Child) -> Child | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            UPDATE children
            SET padron_code = $1,
                medical_record_code = $2,
                dni = $3,
                first_names = $4,
                last_names = $5,
                birth_date = $6,
                gender = $7,
                birth_condition = $8,
                mother_name = $9,
                mother_dni = $10,
                address = $11,
                contact_phone = $12,
                insurance = $13,
                health_facility_id = $14,
                active = $15
            WHERE id = $16
            RETURNING id, padron_code, medical_record_code, dni,
                      first_names, last_names, birth_date, gender, birth_condition,
                      mother_name, mother_dni, address, contact_phone, insurance,
                      health_facility_id, active, registered_by,
                      created_at, updated_at
            """,
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
            child.id,
        )

        if row is None:
            return None

        return Child.from_row(row)

    finally:
        await conn.close()
