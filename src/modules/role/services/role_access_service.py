from uuid import UUID

from ....core.security.access_error import AccessDeniedError
from ...permission.services.permissions_service import permissionService
from ..domain.role_domain import Role


async def caller_access(caller_id: UUID) -> tuple[UUID | None, set[UUID]]:
    return await permissionService.user_access(caller_id)


async def ensure_can_grant(caller_id: UUID, permission_ids: list[UUID]) -> None:
    _, mine = await caller_access(caller_id)

    if not set(permission_ids) <= mine:
        raise AccessDeniedError("No puedes otorgar permisos que tu no tienes")


async def ensure_can_assign(caller_id: UUID, role: Role) -> None:
    _, mine = await caller_access(caller_id)

    if not set(role.permission_ids) <= mine:
        raise AccessDeniedError(f"No puedes asignar el rol '{role.name}' porque tiene permisos que tu no tienes")


async def ensure_can_manage_role(caller_id: UUID, role: Role) -> None:
    _, mine = await caller_access(caller_id)

    if not set(role.permission_ids) <= mine:
        raise AccessDeniedError(f"No puedes modificar el rol '{role.name}' porque tiene permisos que tu no tienes")
