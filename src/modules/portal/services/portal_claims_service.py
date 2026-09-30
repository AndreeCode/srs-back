from uuid import UUID

from ...child.services.children_service import childService
from ...claim.domain.claim_domain import Claim
from ...claim.services.claims_service import claimService
from ...claim_evidence.domain.claim_evidence_domain import ClaimEvidence
from ...claim_evidence.services.claim_evidences_service import claimEvidenceService
from ..domain.portal_errors import PortalNotFoundError
from .portal_access_service import ensure_own_child, ensure_own_claim


async def list_claims(user_id: UUID) -> dict:
    claims = await claimService.get_all(None, user_id, None)
    evidences = []

    for claim in claims:
        evidences += await claimEvidenceService.get_all(claim.id)

    return {
        "claims": [claim.to_dict() for claim in claims],
        "evidences": [evidence.to_dict() for evidence in evidences],
    }


async def create_claim(user_id: UUID, claim: Claim) -> Claim:
    guardian = await ensure_own_child(user_id, claim.child_id)
    child = await childService.get_by_id(claim.child_id)

    claim.requester_user_id = user_id
    claim.requester_dni = guardian.dni

    if claim.health_facility_id is None and child is not None:
        claim.health_facility_id = child.health_facility_id

    return await claimService.create(claim)


async def upload_evidence(user_id: UUID, claim_id: UUID, original_name: str, content: bytes) -> ClaimEvidence:
    await ensure_own_claim(user_id, claim_id)
    return await claimEvidenceService.create(claim_id, original_name, content)


async def get_evidence(user_id: UUID, evidence_id: UUID) -> ClaimEvidence:
    evidence = await claimEvidenceService.get_by_id(evidence_id)

    if evidence is None:
        raise PortalNotFoundError("Evidencia no encontrada")

    await ensure_own_claim(user_id, evidence.claim_id)
    return evidence
