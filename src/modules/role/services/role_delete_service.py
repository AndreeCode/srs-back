from uuid import UUID

from ..repositories.role_repositories import roleRepository


async def delete(role_id: UUID) -> str:
    return await roleRepository.delete(role_id)
