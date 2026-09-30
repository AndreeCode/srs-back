from ..domain.user_domain import User
from ..repositories.user_repositories import userRepository
from .user_validate_role_service import validate_role_and_regions


async def create(user: User) -> User:
    await validate_role_and_regions(user.role_id, user.region_ids, require_active=True)
    return await userRepository.create(user)
