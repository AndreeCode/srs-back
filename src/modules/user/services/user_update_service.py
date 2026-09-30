from ..domain.user_domain import User
from ..repositories.user_repositories import userRepository
from .user_validate_role_service import validate_role_and_regions


async def update(user: User, current: User) -> User | None:
    role_changed = user.role_id != current.role_id
    regions_changed = set(user.region_ids) != set(current.region_ids)

    if role_changed or regions_changed:
        await validate_role_and_regions(user.role_id, user.region_ids, require_active=role_changed)

    return await userRepository.update(user)
