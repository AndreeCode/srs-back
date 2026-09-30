from ....core.db.connection import get_connection
from ..domain.user_domain import User


async def get_all_users() -> list[User]:
    conn = await get_connection()

    try:
        rows = await conn.fetch(
            """
            SELECT id, username, password_hash, role_id, full_name,
                   dni, phone, email,
                   terms_accepted, terms_version, terms_accepted_at,
                   active, blocked, blocked_reason,
                   created_at, updated_at,
                   ARRAY(
                       SELECT ur.region_id FROM user_region ur
                       WHERE ur.user_id = users.id
                       ORDER BY ur.region_id
                   ) AS region_ids
            FROM users
            WHERE active = true
            ORDER BY full_name
            """
        )

        return [User.from_row(row) for row in rows]

    finally:
        await conn.close()
