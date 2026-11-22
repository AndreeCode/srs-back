from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.claim_evidence_domain import ClaimEvidence


async def get_all_claim_evidences(claim_id: UUID | None) -> list[ClaimEvidence]:
    conn = await get_connection()

    try:
        rows = await conn.fetch(
            """
            SELECT id, claim_id, original_name, storage_path, mime_type, size_bytes, created_at, sha256
            FROM claim_evidences
            WHERE ($1::uuid IS NULL OR claim_id = $1)
            ORDER BY claim_id, created_at
            """,
            claim_id,
        )

        return [ClaimEvidence.from_row(row) for row in rows]

    finally:
        await conn.close()
