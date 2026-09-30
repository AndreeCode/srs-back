from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.claim_domain import Claim


async def get_claim_by_id(claim_id: UUID) -> Claim | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            SELECT id, child_id, requester_user_id, requester_dni, child_dni, child_identifier,
                   health_facility_id, service_id, attention_date, message,
                   status, response, reviewed_by, reviewed_at, created_at, updated_at
            FROM claims
            WHERE id = $1
            """,
            claim_id,
        )

        if row is None:
            return None

        return Claim.from_row(row)

    finally:
        await conn.close()
