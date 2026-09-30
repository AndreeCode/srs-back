from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.care_service_domain import CareService


async def get_all_care_services(package_id: UUID | None) -> list[CareService]:
    conn = await get_connection()

    try:
        rows = await conn.fetch(
            """
            SELECT id, package_id, code, name,
                   group_name, group_order, sort_order,
                   min_age_days, max_age_days, min_interval_days, active,
                   created_at, updated_at
            FROM care_services
            WHERE active = true
              AND ($1::uuid IS NULL OR package_id = $1)
            ORDER BY package_id, group_order, sort_order
            """,
            package_id,
        )

        return [CareService.from_row(row) for row in rows]

    finally:
        await conn.close()
