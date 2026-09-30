from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.user_region_domain import UserRegion


async def get_user_region_by_id(user_id: UUID, region_id: UUID) -> UserRegion | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            "SELECT user_id, region_id FROM user_region WHERE user_id = $1 AND region_id = $2",
            user_id,
            region_id,
        )

        if row is None:
            return None

        return UserRegion.from_row(row)

    finally:
        await conn.close()
