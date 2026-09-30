from uuid import UUID

from ..repositories.permission_repositories import permissionRepository


async def user_has(user_id: UUID, code: str) -> bool:
    return await permissionRepository.user_has(user_id, code)
