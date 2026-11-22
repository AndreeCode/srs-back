from uuid import UUID

from ....core.db.connection import get_connection


async def set_claim_evidence_sha256(claim_evidence_id: UUID, sha256: str) -> None:
    conn = await get_connection()

    try:
        await conn.execute(
            "UPDATE claim_evidences SET sha256 = $2 WHERE id = $1 AND sha256 IS NULL", claim_evidence_id, sha256
        )

    finally:
        await conn.close()
