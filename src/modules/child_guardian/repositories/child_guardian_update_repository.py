from ....core.db.connection import get_connection
from ..domain.child_guardian_domain import ChildGuardian


async def update_child_guardian(child_guardian: ChildGuardian) -> ChildGuardian | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            UPDATE child_guardian
            SET relationship = $1
            WHERE child_id = $2 AND guardian_id = $3
            RETURNING child_id, guardian_id, relationship, verified, requested_at, verified_by, verified_at
            """,
            child_guardian.relationship,
            child_guardian.child_id,
            child_guardian.guardian_id,
        )

        if row is None:
            return None

        return ChildGuardian.from_row(row)

    finally:
        await conn.close()
