from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.health_facility_domain import HealthFacility


async def get_all_health_facilities(region_id: UUID | None) -> list[HealthFacility]:
    conn = await get_connection()

    try:
        rows = await conn.fetch(
            """
            SELECT id, name, region_id, active, created_at
            FROM health_facilities
            WHERE active = true
              AND ($1::uuid IS NULL OR region_id = $1)
            ORDER BY name
            """,
            region_id,
        )

        return [HealthFacility.from_row(row) for row in rows]

    finally:
        await conn.close()
