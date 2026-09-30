from uuid import UUID

from ..domain.guardian_domain import Guardian
from ..repositories.guardian_repositories import guardianRepository


async def get_by_id(guardian_id: UUID) -> Guardian | None:
    return await guardianRepository.get_by_id(guardian_id)
