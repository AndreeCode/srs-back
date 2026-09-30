from ...child.services.children_service import childService
from ..domain.claim_domain import Claim
from ..domain.claim_errors import ClaimValidationError
from ..repositories.claim_repositories import claimRepository
from .claim_validate_service import validate_claim


async def create(claim: Claim) -> Claim:
    child = await childService.get_by_id(claim.child_id)

    if child is None:
        raise ClaimValidationError("El child_id indicado no existe")

    if not child.active:
        raise ClaimValidationError("El nino indicado esta inactivo")

    if not claim.child_identifier:
        claim.child_identifier = child.padron_code

    if claim.child_dni is None:
        claim.child_dni = child.dni

    await validate_claim(claim, None)
    return await claimRepository.create(claim)
