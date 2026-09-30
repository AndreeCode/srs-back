from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.child_control_domain import ChildControl


async def get_child_control_by_id(child_control_id: UUID) -> ChildControl | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            SELECT id, child_id, service_id, status, scheduled_date, completed_date,
                   health_facility_id, batch_number, book_page, book_record, notes, registered_by,
                   created_at, updated_at
            FROM child_controls
            WHERE id = $1
            """,
            child_control_id,
        )

        if row is None:
            return None

        return ChildControl.from_row(row)

    finally:
        await conn.close()
