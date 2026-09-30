from uuid import UUID

from ..domain.claim_evidence_domain import ClaimEvidence
from ..repositories.claim_evidence_repositories import claimEvidenceRepository


async def get_all(claim_id: UUID | None) -> list[ClaimEvidence]:
    return await claimEvidenceRepository.get_all(claim_id)
