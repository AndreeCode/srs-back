from ..domain.role_domain import Role
from ..repositories.role_repositories import roleRepository


async def get_all() -> list[Role]:
    return await roleRepository.get_all()
