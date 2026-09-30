from ....core.db.connection import get_connection
from ..domain.role_domain import Role


async def get_all_roles() -> list[Role]:
    conn = await get_connection()

    try:
        rows = await conn.fetch(
            """
            SELECT id, name, is_active,
                   ARRAY(
                       SELECT rp.permission_id FROM role_permission rp
                       WHERE rp.role_id = roles.id
                       ORDER BY rp.permission_id
                   ) AS permission_ids
            FROM roles
            WHERE is_active = true
            ORDER BY name
            """
        )

        return [Role.from_row(row) for row in rows]

    finally:
        await conn.close()
