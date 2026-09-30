from ..domain.guardian_domain import Guardian
from ..repositories.guardian_repositories import guardianRepository
from .guardian_validate_user_service import validate_guardian_user


async def create(guardian: Guardian) -> Guardian:
    await validate_guardian_user(guardian.user_id)
    return await guardianRepository.create(guardian)
