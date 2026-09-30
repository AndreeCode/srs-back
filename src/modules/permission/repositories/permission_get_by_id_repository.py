from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.permission_domain import Permission


async def get_permission_by_id(permission_id: UUID) -> Permission | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            "SELECT id, code, description FROM permissions WHERE id = $1",
            permission_id,
        )

        if row is None:
            return None

        return Permission.from_row(row)

    finally:
        await conn.close()
