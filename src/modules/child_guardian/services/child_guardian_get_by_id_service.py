from uuid import UUID

from ..domain.child_guardian_domain import ChildGuardian
from ..repositories.child_guardian_repositories import childGuardianRepository


async def get_by_id(child_id: UUID, guardian_id: UUID) -> ChildGuardian | None:
    return await childGuardianRepository.get_by_id(child_id, guardian_id)
