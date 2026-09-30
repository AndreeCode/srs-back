from ..domain.permission_domain import Permission
from ..repositories.permission_repositories import permissionRepository


async def create(permission: Permission) -> Permission:
    return await permissionRepository.create(permission)
