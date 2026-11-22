from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.guardian_his_child_domain import GuardianHisChild


async def get_all_guardian_his_children(guardian_id: UUID | None, document_number: str | None) -> list[GuardianHisChild]:
    conn = await get_connection()

    try:
        rows = await conn.fetch(
            """
            SELECT guardian_id, document_number, birth_date, relationship, child_name, linked_by, created_at,
                   verified, verified_by, verified_at
            FROM guardian_his_children
            WHERE ($1::uuid IS NULL OR guardian_id = $1)
              AND ($2::text IS NULL OR document_number = $2)
            ORDER BY birth_date
            """,
            guardian_id,
            document_number,
        )

        return [GuardianHisChild.from_row(row) for row in rows]

    finally:
        await conn.close()
