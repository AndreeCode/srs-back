from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.region_domain import Region


async def get_region_by_id(region_id: UUID) -> Region | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            "SELECT id, name, health_network, active FROM regions WHERE id = $1",
            region_id,
        )

        if row is None:
            return None

        return Region.from_row(row)

    finally:
        await conn.close()
