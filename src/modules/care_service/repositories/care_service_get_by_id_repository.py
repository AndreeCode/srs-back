from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.care_service_domain import CareService


async def get_care_service_by_id(care_service_id: UUID) -> CareService | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            SELECT id, package_id, code, name,
                   group_name, group_order, sort_order,
                   min_age_days, max_age_days, min_interval_days, active,
                   created_at, updated_at
            FROM care_services
            WHERE id = $1
            """,
            care_service_id,
        )

        if row is None:
            return None

        return CareService.from_row(row)

    finally:
        await conn.close()
