from ....core.db.connection import get_connection
from ..domain.user_domain import User


async def get_user_by_username(username: str) -> User | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
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
            WHERE username = $1
            """,
            username,
        )

        if row is None:
            return None

        return User.from_row(row)

    finally:
        await conn.close()
