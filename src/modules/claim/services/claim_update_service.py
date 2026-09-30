from ..domain.claim_domain import Claim
from ..repositories.claim_repositories import claimRepository
from .claim_validate_service import validate_claim


async def update(claim: Claim, current: Claim) -> Claim | None:
    await validate_claim(claim, current)
    return await claimRepository.update(claim)
