from uuid import UUID

from ..domain.claim_domain import Claim
from ..repositories.claim_repositories import claimRepository


async def get_by_id(claim_id: UUID) -> Claim | None:
    return await claimRepository.get_by_id(claim_id)
