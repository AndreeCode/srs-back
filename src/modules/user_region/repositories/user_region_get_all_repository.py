from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.user_region_domain import UserRegion


async def get_all_user_regions(user_id: UUID | None, region_id: UUID | None) -> list[UserRegion]:
    conn = await get_connection()

    try:
        rows = await conn.fetch(
            """
            SELECT user_id, region_id
            FROM user_region
            WHERE ($1::uuid IS NULL OR user_id = $1)
              AND ($2::uuid IS NULL OR region_id = $2)
            ORDER BY user_id, region_id
            """,
            user_id,
            region_id,
        )

        return [UserRegion.from_row(row) for row in rows]

    finally:
        await conn.close()
