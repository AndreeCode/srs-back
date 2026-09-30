from uuid import UUID

from ..repositories.child_guardian_repositories import childGuardianRepository


async def delete(child_id: UUID, guardian_id: UUID) -> str:
    return await childGuardianRepository.delete(child_id, guardian_id)
