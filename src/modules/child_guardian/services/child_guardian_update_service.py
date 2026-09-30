from ..domain.child_guardian_domain import ChildGuardian
from ..repositories.child_guardian_repositories import childGuardianRepository


async def update(child_guardian: ChildGuardian) -> ChildGuardian | None:
    return await childGuardianRepository.update(child_guardian)
