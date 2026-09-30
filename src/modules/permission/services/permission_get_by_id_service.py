from uuid import UUID

from ..domain.permission_domain import Permission
from ..repositories.permission_repositories import permissionRepository


async def get_by_id(permission_id: UUID) -> Permission | None:
    return await permissionRepository.get_by_id(permission_id)
