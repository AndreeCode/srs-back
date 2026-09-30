from ..domain.role_domain import Role
from ..repositories.role_repositories import roleRepository


async def create(role: Role) -> Role:
    return await roleRepository.create(role)
