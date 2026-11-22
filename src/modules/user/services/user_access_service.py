from uuid import UUID

from ....core.security.access_error import AccessDeniedError
from ...role.services.role_access_service import caller_access
from ...role.services.roles_service import roleService
from ..domain.user_domain import User


async def ensure_can_manage(caller_id: UUID, target: User) -> None:
    if caller_id == target.id:
        return

    role = await roleService.get_by_id(target.role_id)
    _, mine = await caller_access(caller_id)

    if role is not None and not set(role.permission_ids) <= mine:
        raise AccessDeniedError("No puedes modificar a un usuario con mas permisos que tu")
