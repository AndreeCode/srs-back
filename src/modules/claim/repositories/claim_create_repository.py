from ....core.db.connection import get_connection
from ..domain.claim_domain import Claim


async def create_claim(claim: Claim) -> Claim:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            INSERT INTO claims (
                id, child_id, requester_user_id, requester_dni, child_dni, child_identifier,
                health_facility_id, service_id, attention_date, message, status
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            RETURNING id, child_id, requester_user_id, requester_dni, child_dni, child_identifier,
                      health_facility_id, service_id, attention_date, message,
                      status, response, reviewed_by, reviewed_at, created_at, updated_at
            """,
            claim.id,
            claim.child_id,
            claim.requester_user_id,
            claim.requester_dni,
            claim.child_dni,
            claim.child_identifier,
            claim.health_facility_id,
            claim.service_id,
            claim.attention_date,
            claim.message,
            claim.status,
        )

        return Claim.from_row(row)

    finally:
        await conn.close()
