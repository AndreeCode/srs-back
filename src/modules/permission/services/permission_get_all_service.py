from ..domain.permission_domain import Permission
from ..repositories.permission_repositories import permissionRepository


async def get_all() -> list[Permission]:
    return await permissionRepository.get_all()
