from ....core.db.connection import get_connection
from ..domain.guardian_his_child_domain import GuardianHisChild


async def create_guardian_his_child(link: GuardianHisChild) -> GuardianHisChild | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            INSERT INTO guardian_his_children (guardian_id, document_number, birth_date, relationship, child_name, linked_by)
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (guardian_id, document_number) DO NOTHING
            RETURNING guardian_id, document_number, birth_date, relationship, child_name, linked_by, created_at
            """,
            link.guardian_id,
            link.document_number,
            link.birth_date,
            link.relationship,
            link.child_name,
            link.linked_by,
        )

        return GuardianHisChild.from_row(row) if row else None

    finally:
        await conn.close()
