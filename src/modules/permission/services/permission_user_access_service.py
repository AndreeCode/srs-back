from uuid import UUID

from ..repositories.permission_repositories import permissionRepository


async def user_access(user_id: UUID) -> tuple[UUID | None, set[UUID]]:
    return await permissionRepository.user_access(user_id)
