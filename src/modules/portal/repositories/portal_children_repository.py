from uuid import UUID

from ....core.db.connection import get_connection
from ...child.domain.child_domain import Child


async def get_children_of_guardian(guardian_id: UUID) -> list[tuple[Child, str]]:
    conn = await get_connection()

    try:
        rows = await conn.fetch(
            """
            SELECT c.id, c.padron_code, c.medical_record_code, c.dni, c.first_names, c.last_names,
                   c.birth_date, c.gender, c.birth_condition, c.mother_name, c.mother_dni, c.address,
                   c.contact_phone, c.insurance, c.health_facility_id, c.active, c.registered_by,
                   c.created_at, c.updated_at, cg.relationship
            FROM child_guardian cg
            JOIN children c ON c.id = cg.child_id
            WHERE cg.guardian_id = $1 AND cg.verified AND c.active = true
            ORDER BY c.birth_date
            """,
            guardian_id,
        )

        return [(Child.from_row(row), row["relationship"]) for row in rows]

    finally:
        await conn.close()


async def get_pending_children_of_guardian(guardian_id: UUID) -> list[tuple[Child, str, object]]:
    conn = await get_connection()

    try:
        rows = await conn.fetch(
            """
            SELECT c.id, c.padron_code, c.medical_record_code, c.dni, c.first_names, c.last_names,
                   c.birth_date, c.gender, c.birth_condition, c.mother_name, c.mother_dni, c.address,
                   c.contact_phone, c.insurance, c.health_facility_id, c.active, c.registered_by,
                   c.created_at, c.updated_at, cg.relationship, cg.requested_at
            FROM child_guardian cg
            JOIN children c ON c.id = cg.child_id
            WHERE cg.guardian_id = $1 AND NOT cg.verified AND c.active = true
            ORDER BY cg.requested_at
            """,
            guardian_id,
        )

        return [(Child.from_row(row), row["relationship"], row["requested_at"]) for row in rows]

    finally:
        await conn.close()
