from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.child_control_domain import ChildControl


async def get_all_child_controls(
    child_id: UUID | None,
    service_id: UUID | None,
    status: str | None,
) -> list[ChildControl]:
    conn = await get_connection()

    try:
        rows = await conn.fetch(
            """
            SELECT cc.id, cc.child_id, cc.service_id, cc.status, cc.scheduled_date, cc.completed_date,
                   cc.health_facility_id, cc.batch_number, cc.book_page, cc.book_record, cc.notes,
                   cc.registered_by, cc.created_at, cc.updated_at
            FROM child_controls cc
            JOIN care_services cs ON cs.id = cc.service_id
            WHERE ($1::uuid IS NULL OR cc.child_id = $1)
              AND ($2::uuid IS NULL OR cc.service_id = $2)
              AND ($3::control_status IS NULL OR cc.status = $3::control_status)
            ORDER BY cc.child_id, cs.min_age_days, cs.group_order, cs.sort_order
            """,
            child_id,
            service_id,
            status,
        )

        return [ChildControl.from_row(row) for row in rows]

    finally:
        await conn.close()
