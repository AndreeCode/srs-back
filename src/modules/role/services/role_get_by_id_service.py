from uuid import UUID

from ..domain.role_domain import Role
from ..repositories.role_repositories import roleRepository


async def get_by_id(role_id: UUID) -> Role | None:
    return await roleRepository.get_by_id(role_id)
