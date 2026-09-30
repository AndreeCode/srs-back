from ..domain.permission_domain import Permission
from ..repositories.permission_repositories import permissionRepository


async def update(permission: Permission) -> Permission | None:
    return await permissionRepository.update(permission)
