from uuid import UUID

from ....core.db.connection import get_connection


async def delete_claim_evidence(claim_evidence_id: UUID) -> str | None:
    conn = await get_connection()

    try:
        return await conn.fetchval(
            "DELETE FROM claim_evidences WHERE id = $1 RETURNING storage_path",
            claim_evidence_id,
        )

    finally:
        await conn.close()
