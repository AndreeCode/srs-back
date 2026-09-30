from uuid import UUID

from ..repositories.guardian_repositories import guardianRepository


async def delete(guardian_id: UUID) -> str:
    return await guardianRepository.delete(guardian_id)
