from ....core.db.connection import get_connection
from ..domain.child_guardian_domain import ChildGuardian


async def create_child_guardian(child_guardian: ChildGuardian) -> ChildGuardian:
    conn = await get_connection()

    try:
        if child_guardian.relationship is None:
            row = await conn.fetchrow(
                """
                INSERT INTO child_guardian (child_id, guardian_id, verified)
                VALUES ($1, $2, $3)
                RETURNING child_id, guardian_id, relationship, verified, requested_at, verified_by, verified_at
                """,
                child_guardian.child_id,
                child_guardian.guardian_id,
                child_guardian.verified,
            )
        else:
            row = await conn.fetchrow(
                """
                INSERT INTO child_guardian (child_id, guardian_id, relationship, verified)
                VALUES ($1, $2, $3, $4)
                RETURNING child_id, guardian_id, relationship, verified, requested_at, verified_by, verified_at
                """,
                child_guardian.child_id,
                child_guardian.guardian_id,
                child_guardian.relationship,
                child_guardian.verified,
            )

        return ChildGuardian.from_row(row)

    finally:
        await conn.close()
