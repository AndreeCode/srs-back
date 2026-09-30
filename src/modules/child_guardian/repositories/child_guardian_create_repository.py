from ....core.db.connection import get_connection
from ..domain.child_guardian_domain import ChildGuardian


async def create_child_guardian(child_guardian: ChildGuardian) -> ChildGuardian:
    conn = await get_connection()

    try:
        if child_guardian.relationship is None:
            row = await conn.fetchrow(
                """
                INSERT INTO child_guardian (child_id, guardian_id)
                VALUES ($1, $2)
                RETURNING child_id, guardian_id, relationship
                """,
                child_guardian.child_id,
                child_guardian.guardian_id,
            )
        else:
            row = await conn.fetchrow(
                """
                INSERT INTO child_guardian (child_id, guardian_id, relationship)
                VALUES ($1, $2, $3)
                RETURNING child_id, guardian_id, relationship
                """,
                child_guardian.child_id,
                child_guardian.guardian_id,
                child_guardian.relationship,
            )

        return ChildGuardian.from_row(row)

    finally:
        await conn.close()
