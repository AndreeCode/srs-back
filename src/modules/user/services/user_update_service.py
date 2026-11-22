from uuid import UUID

from ....core.security.access_error import AccessDeniedError
from ...role.services.role_access_service import ensure_can_assign
from ...role.services.roles_service import roleService
from ..domain.user_domain import User
from ...session.repositories.session_repositories import sessionRepository
from ..repositories.user_repositories import userRepository
from .user_access_service import ensure_can_manage
from .user_validate_role_service import validate_role_and_regions


async def update(caller_id: UUID, user: User, current: User) -> User | None:
    await ensure_can_manage(caller_id, current)

    is_self = caller_id == current.id
    role_changed = user.role_id != current.role_id
    regions_changed = set(user.region_ids) != set(current.region_ids)

    if is_self:
        if role_changed:
            raise AccessDeniedError("No puedes cambiar tu propio rol")
        if current.active and not user.active:
            raise AccessDeniedError("No puedes desactivar tu propia cuenta")
        if user.blocked and not current.blocked:
            raise AccessDeniedError("No puedes bloquear tu propia cuenta")

    if role_changed or regions_changed:
        await validate_role_and_regions(user.role_id, user.region_ids, require_active=role_changed)

    if role_changed:
        await ensure_can_assign(caller_id, await roleService.get_by_id(user.role_id))

    updated = await userRepository.update(user)

    if updated is not None:
        if user.password_hash != current.password_hash:
            await sessionRepository.revoke_all_of_user(current.id, "password_reset")
            if not is_self:
                await userRepository.mark_temporary(current.id)
        elif (user.blocked and not current.blocked) or (current.active and not user.active):
            await sessionRepository.revoke_all_of_user(current.id, "user_blocked" if user.blocked else "user_deactivated")

    return updated
