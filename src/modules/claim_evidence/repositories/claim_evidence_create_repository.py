from ....core.db.connection import get_connection
from ..domain.claim_evidence_domain import ClaimEvidence


async def create_claim_evidence(claim_evidence: ClaimEvidence) -> ClaimEvidence:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            INSERT INTO claim_evidences (id, claim_id, original_name, storage_path, mime_type, size_bytes, sha256)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING id, claim_id, original_name, storage_path, mime_type, size_bytes, created_at, sha256
            """,
            claim_evidence.id,
            claim_evidence.claim_id,
            claim_evidence.original_name,
            claim_evidence.storage_path,
            claim_evidence.mime_type,
            claim_evidence.size_bytes,
            claim_evidence.sha256,
        )

        return ClaimEvidence.from_row(row)

    finally:
        await conn.close()
