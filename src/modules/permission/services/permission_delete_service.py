from uuid import UUID

from ..repositories.permission_repositories import permissionRepository


async def delete(permission_id: UUID) -> str:
    return await permissionRepository.delete(permission_id)
