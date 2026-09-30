from uuid import UUID

from ...role.services.roles_service import roleService
from ...user.services.users_service import userService
from ..domain.guardian_errors import GuardianValidationError


async def validate_guardian_user(user_id: UUID | None) -> None:
    if user_id is None:
        return

    user = await userService.get_by_id(user_id)

    if user is None:
        raise GuardianValidationError("El user_id indicado no existe")

    role = await roleService.get_by_id(user.role_id)

    if role is None or role.name != "guardian":
        raise GuardianValidationError("El usuario vinculado debe tener el rol guardian")
