from ....core.db.connection import get_connection
from ..domain.child_control_domain import ChildControl


async def update_child_control(child_control: ChildControl) -> ChildControl | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            UPDATE child_controls
            SET status = $1,
                scheduled_date = $2,
                completed_date = $3,
                health_facility_id = $4,
                batch_number = $5,
                book_page = $6,
                book_record = $7,
                notes = $8
            WHERE id = $9
            RETURNING id, child_id, service_id, status, scheduled_date, completed_date,
                      health_facility_id, batch_number, book_page, book_record, notes, registered_by,
                      created_at, updated_at
            """,
            child_control.status,
            child_control.scheduled_date,
            child_control.completed_date,
            child_control.health_facility_id,
            child_control.batch_number,
            child_control.book_page,
            child_control.book_record,
            child_control.notes,
            child_control.id,
        )

        if row is None:
            return None

        return ChildControl.from_row(row)

    finally:
        await conn.close()
