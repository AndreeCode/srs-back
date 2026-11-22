from uuid import UUID

from ....core.security.access_error import AccessDeniedError
from ..repositories.role_repositories import roleRepository
from .role_access_service import caller_access, ensure_can_manage_role


async def delete(caller_id: UUID, role_id: UUID) -> str:
    role = await roleRepository.get_by_id(role_id)

    if role is None:
        return "not_found"

    own_role_id, _ = await caller_access(caller_id)
    if role.id == own_role_id:
        raise AccessDeniedError("No puedes eliminar tu propio rol")

    await ensure_can_manage_role(caller_id, role)
    return await roleRepository.delete(role_id)
