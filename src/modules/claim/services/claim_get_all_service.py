from uuid import UUID

from ..domain.claim_domain import Claim
from ..repositories.claim_repositories import claimRepository


async def get_all(child_id: UUID | None, requester_user_id: UUID | None, status: str | None) -> list[Claim]:
    return await claimRepository.get_all(child_id, requester_user_id, status)
