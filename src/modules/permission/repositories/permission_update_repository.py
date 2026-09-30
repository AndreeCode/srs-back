from ....core.db.connection import get_connection
from ..domain.permission_domain import Permission


async def update_permission(permission: Permission) -> Permission | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            UPDATE permissions
            SET code = $1, description = $2
            WHERE id = $3
            RETURNING id, code, description
            """,
            permission.code,
            permission.description,
            permission.id,
        )

        if row is None:
            return None

        return Permission.from_row(row)

    finally:
        await conn.close()
