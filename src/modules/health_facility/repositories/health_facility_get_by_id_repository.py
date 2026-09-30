from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.health_facility_domain import HealthFacility


async def get_health_facility_by_id(health_facility_id: UUID) -> HealthFacility | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            SELECT id, name, region_id, active, created_at
            FROM health_facilities
            WHERE id = $1
            """,
            health_facility_id,
        )

        if row is None:
            return None

        return HealthFacility.from_row(row)

    finally:
        await conn.close()
