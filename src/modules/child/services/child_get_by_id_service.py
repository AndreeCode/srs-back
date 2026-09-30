from uuid import UUID

from ..domain.child_domain import Child
from ..repositories.child_repositories import childRepository


async def get_by_id(child_id: UUID) -> Child | None:
    return await childRepository.get_by_id(child_id)
