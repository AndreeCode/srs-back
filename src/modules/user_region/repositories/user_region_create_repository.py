from ....core.db.connection import get_connection
from ..domain.user_region_domain import UserRegion


async def create_user_region(user_region: UserRegion) -> UserRegion:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            INSERT INTO user_region (user_id, region_id)
            VALUES ($1, $2)
            RETURNING user_id, region_id
            """,
            user_region.user_id,
            user_region.region_id,
        )

        return UserRegion.from_row(row)

    finally:
        await conn.close()
