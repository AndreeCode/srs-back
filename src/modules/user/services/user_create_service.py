from uuid import UUID

from ...role.services.role_access_service import ensure_can_assign
from ...role.services.roles_service import roleService
from ..domain.user_domain import User
from ..repositories.user_repositories import userRepository
from .user_validate_role_service import validate_role_and_regions


async def create(user: User, caller_id: UUID | None = None) -> User:
    await validate_role_and_regions(user.role_id, user.region_ids, require_active=True)

    if caller_id is not None:
        await ensure_can_assign(caller_id, await roleService.get_by_id(user.role_id))

    created = await userRepository.create(user)

    if caller_id is not None:
        await userRepository.mark_temporary(created.id)

    return created
