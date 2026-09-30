from ....core.db.connection import get_connection
from ..domain.region_domain import Region


async def get_all_regions() -> list[Region]:
    conn = await get_connection()

    try:
        rows = await conn.fetch(
            """
            SELECT id, name, health_network, active
            FROM regions
            WHERE active = true
            ORDER BY name
            """
        )

        return [Region.from_row(row) for row in rows]

    finally:
        await conn.close()
