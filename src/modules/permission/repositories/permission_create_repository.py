from ....core.db.connection import get_connection
from ..domain.permission_domain import Permission


async def create_permission(permission: Permission) -> Permission:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            INSERT INTO permissions (id, code, description)
            VALUES ($1, $2, $3)
            RETURNING id, code, description
            """,
            permission.id,
            permission.code,
            permission.description,
        )

        return Permission.from_row(row)

    finally:
        await conn.close()
