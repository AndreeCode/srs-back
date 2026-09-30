from ....core.db.connection import get_connection
from ..domain.child_control_domain import ChildControl


async def create_child_control(child_control: ChildControl) -> ChildControl:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            INSERT INTO child_controls (
                id, child_id, service_id, status, scheduled_date, completed_date,
                health_facility_id, batch_number, book_page, book_record, notes, registered_by
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
            RETURNING id, child_id, service_id, status, scheduled_date, completed_date,
                      health_facility_id, batch_number, book_page, book_record, notes, registered_by,
                      created_at, updated_at
            """,
            child_control.id,
            child_control.child_id,
            child_control.service_id,
            child_control.status,
            child_control.scheduled_date,
            child_control.completed_date,
            child_control.health_facility_id,
            child_control.batch_number,
            child_control.book_page,
            child_control.book_record,
            child_control.notes,
            child_control.registered_by,
        )

        return ChildControl.from_row(row)

    finally:
        await conn.close()
