from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.claim_domain import Claim


async def get_all_claims(
    child_id: UUID | None,
    requester_user_id: UUID | None,
    status: str | None,
) -> list[Claim]:
    conn = await get_connection()

    try:
        rows = await conn.fetch(
            """
            SELECT id, child_id, requester_user_id, requester_dni, child_dni, child_identifier,
                   health_facility_id, service_id, attention_date, message,
                   status, response, reviewed_by, reviewed_at, created_at, updated_at
            FROM claims
            WHERE ($1::uuid IS NULL OR child_id = $1)
              AND ($2::uuid IS NULL OR requester_user_id = $2)
              AND ($3::claim_status IS NULL OR status = $3::claim_status)
            ORDER BY created_at DESC
            """,
            child_id,
            requester_user_id,
            status,
        )

        return [Claim.from_row(row) for row in rows]

    finally:
        await conn.close()
