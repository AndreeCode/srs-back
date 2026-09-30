from ....core.db.connection import get_connection
from ..domain.permission_domain import Permission


async def get_all_permissions() -> list[Permission]:
    conn = await get_connection()

    try:
        rows = await conn.fetch("SELECT id, code, description FROM permissions ORDER BY code")
        return [Permission.from_row(row) for row in rows]

    finally:
        await conn.close()
