from uuid import UUID

from ..domain.child_guardian_domain import ChildGuardian
from ..repositories.child_guardian_repositories import childGuardianRepository


async def get_all(child_id: UUID | None, guardian_id: UUID | None) -> list[ChildGuardian]:
    return await childGuardianRepository.get_all(child_id, guardian_id)
