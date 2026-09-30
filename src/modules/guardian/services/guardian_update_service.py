from ..domain.guardian_domain import Guardian
from ..repositories.guardian_repositories import guardianRepository
from .guardian_validate_user_service import validate_guardian_user


async def update(guardian: Guardian, current: Guardian) -> Guardian | None:
    if guardian.user_id != current.user_id:
        await validate_guardian_user(guardian.user_id)

    return await guardianRepository.update(guardian)
