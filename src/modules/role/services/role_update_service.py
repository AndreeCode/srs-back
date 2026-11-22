from uuid import UUID

from ....core.security.access_error import AccessDeniedError
from ..domain.role_domain import Role
from ..repositories.role_repositories import roleRepository
from .role_access_service import caller_access, ensure_can_grant, ensure_can_manage_role


async def update(caller_id: UUID, role: Role, current: Role) -> Role | None:
    if role.name != current.name:
        raise AccessDeniedError("El nombre de un rol no se puede cambiar: el sistema lo usa para decidir el acceso")

    await ensure_can_manage_role(caller_id, current)
    await ensure_can_grant(caller_id, role.permission_ids)

    own_role_id, _ = await caller_access(caller_id)
    if current.id == own_role_id:
        if not role.is_active:
            raise AccessDeniedError("No puedes desactivar tu propio rol")
        if set(current.permission_ids) - set(role.permission_ids):
            raise AccessDeniedError("No puedes quitarle permisos a tu propio rol")

    return await roleRepository.update(role)
