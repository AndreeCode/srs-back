from ..domain.guardian_domain import Guardian
from ..repositories.guardian_repositories import guardianRepository


async def get_all() -> list[Guardian]:
    return await guardianRepository.get_all()
