from ..domain.role_domain import Role
from ..repositories.role_repositories import roleRepository


async def update(role: Role) -> Role | None:
    return await roleRepository.update(role)
