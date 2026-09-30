from ....core.db.connection import get_connection
from ..domain.region_domain import Region


async def create_region(region: Region) -> Region:
    conn = await get_connection()

    try:
        if region.health_network is None:
            row = await conn.fetchrow(
                """
                INSERT INTO regions (id, name, active)
                VALUES ($1, $2, $3)
                RETURNING id, name, health_network, active
                """,
                region.id,
                region.name,
                region.active,
            )
        else:
            row = await conn.fetchrow(
                """
                INSERT INTO regions (id, name, active, health_network)
                VALUES ($1, $2, $3, $4)
                RETURNING id, name, health_network, active
                """,
                region.id,
                region.name,
                region.active,
                region.health_network,
            )

        return Region.from_row(row)

    finally:
        await conn.close()
