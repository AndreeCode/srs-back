from ....core.db.connection import get_connection
from ..domain.health_facility_domain import HealthFacility


async def create_health_facility(health_facility: HealthFacility) -> HealthFacility:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            INSERT INTO health_facilities (id, name, region_id, active)
            VALUES ($1, $2, $3, $4)
            RETURNING id, name, region_id, active, created_at
            """,
            health_facility.id,
            health_facility.name,
            health_facility.region_id,
            health_facility.active,
        )

        return HealthFacility.from_row(row)

    finally:
        await conn.close()
