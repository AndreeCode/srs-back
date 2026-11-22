from uuid import UUID

from ..domain.role_domain import Role
from ..repositories.role_repositories import roleRepository
from .role_access_service import ensure_can_grant


async def create(caller_id: UUID, role: Role) -> Role:
    await ensure_can_grant(caller_id, role.permission_ids)
    return await roleRepository.create(role)
