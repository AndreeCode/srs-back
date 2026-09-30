from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.role_domain import Role


async def get_role_by_id(role_id: UUID) -> Role | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            SELECT id, name, is_active,
                   ARRAY(
                       SELECT rp.permission_id FROM role_permission rp
                       WHERE rp.role_id = roles.id
                       ORDER BY rp.permission_id
                   ) AS permission_ids
            FROM roles
            WHERE id = $1
            """,
            role_id,
        )

        if row is None:
            return None

        return Role.from_row(row)

    finally:
        await conn.close()
