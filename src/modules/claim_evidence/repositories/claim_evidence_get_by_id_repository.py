from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.claim_evidence_domain import ClaimEvidence


async def get_claim_evidence_by_id(claim_evidence_id: UUID) -> ClaimEvidence | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            SELECT id, claim_id, original_name, storage_path, mime_type, size_bytes, created_at
            FROM claim_evidences
            WHERE id = $1
            """,
            claim_evidence_id,
        )

        if row is None:
            return None

        return ClaimEvidence.from_row(row)

    finally:
        await conn.close()
