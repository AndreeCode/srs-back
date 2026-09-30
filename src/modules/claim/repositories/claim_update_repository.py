from ....core.db.connection import get_connection
from ..domain.claim_domain import Claim


async def update_claim(claim: Claim) -> Claim | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            UPDATE claims
            SET health_facility_id = $1,
                service_id = $2,
                attention_date = $3,
                message = $4,
                status = $5,
                response = $6,
                reviewed_by = $7,
                reviewed_at = $8
            WHERE id = $9
            RETURNING id, child_id, requester_user_id, requester_dni, child_dni, child_identifier,
                      health_facility_id, service_id, attention_date, message,
                      status, response, reviewed_by, reviewed_at, created_at, updated_at
            """,
            claim.health_facility_id,
            claim.service_id,
            claim.attention_date,
            claim.message,
            claim.status,
            claim.response,
            claim.reviewed_by,
            claim.reviewed_at,
            claim.id,
        )

        if row is None:
            return None

        return Claim.from_row(row)

    finally:
        await conn.close()
