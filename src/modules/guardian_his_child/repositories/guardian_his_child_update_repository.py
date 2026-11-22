from ....core.db.connection import get_connection
from ..domain.guardian_his_child_domain import GuardianHisChild


async def update_guardian_his_child(link: GuardianHisChild) -> GuardianHisChild | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            UPDATE guardian_his_children
            SET relationship = $3, child_name = $4
            WHERE guardian_id = $1 AND document_number = $2
            RETURNING guardian_id, document_number, birth_date, relationship, child_name, linked_by, created_at
            """,
            link.guardian_id,
            link.document_number,
            link.relationship,
            link.child_name,
        )

        return GuardianHisChild.from_row(row) if row else None

    finally:
        await conn.close()
