from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.child_guardian_domain import ChildGuardian


async def get_all_child_guardians(child_id: UUID | None, guardian_id: UUID | None) -> list[ChildGuardian]:
    conn = await get_connection()

    try:
        rows = await conn.fetch(
            """
            SELECT child_id, guardian_id, relationship
            FROM child_guardian
            WHERE ($1::uuid IS NULL OR child_id = $1)
              AND ($2::uuid IS NULL OR guardian_id = $2)
            ORDER BY child_id, guardian_id
            """,
            child_id,
            guardian_id,
        )

        return [ChildGuardian.from_row(row) for row in rows]

    finally:
        await conn.close()
