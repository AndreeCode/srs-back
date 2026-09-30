from ....core.db.connection import get_connection
from ..domain.health_facility_domain import HealthFacility


async def update_health_facility(health_facility: HealthFacility) -> HealthFacility | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            UPDATE health_facilities
            SET name = $1, region_id = $2, active = $3
            WHERE id = $4
            RETURNING id, name, region_id, active, created_at
            """,
            health_facility.name,
            health_facility.region_id,
            health_facility.active,
            health_facility.id,
        )

        if row is None:
            return None

        return HealthFacility.from_row(row)

    finally:
        await conn.close()
