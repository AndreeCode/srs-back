from uuid import UUID

from ..domain.claim_evidence_domain import ClaimEvidence
from ..repositories.claim_evidence_repositories import claimEvidenceRepository


async def get_by_id(claim_evidence_id: UUID) -> ClaimEvidence | None:
    return await claimEvidenceRepository.get_by_id(claim_evidence_id)
