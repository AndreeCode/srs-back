from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.child_guardian_domain import ChildGuardian


async def get_child_guardian_by_id(child_id: UUID, guardian_id: UUID) -> ChildGuardian | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            SELECT child_id, guardian_id, relationship
            FROM child_guardian
            WHERE child_id = $1 AND guardian_id = $2
            """,
            child_id,
            guardian_id,
        )

        if row is None:
            return None

        return ChildGuardian.from_row(row)

    finally:
        await conn.close()
