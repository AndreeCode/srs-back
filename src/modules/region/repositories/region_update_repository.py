from ....core.db.connection import get_connection
from ..domain.region_domain import Region


async def update_region(region: Region) -> Region | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            UPDATE regions
            SET name = $1, health_network = $2, active = $3
            WHERE id = $4
            RETURNING id, name, health_network, active
            """,
            region.name,
            region.health_network,
            region.active,
            region.id,
        )

        if row is None:
            return None

        return Region.from_row(row)

    finally:
        await conn.close()
