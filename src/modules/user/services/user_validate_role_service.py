from uuid import UUID

from ...role.services.roles_service import roleService
from ..domain.user_errors import UserValidationError


async def validate_role_and_regions(role_id: UUID, region_ids: list[UUID], require_active: bool) -> None:
    role = await roleService.get_by_id(role_id)

    if role is None:
        raise UserValidationError("El role_id indicado no existe")

    if require_active and not role.is_active:
        raise UserValidationError("El rol indicado esta inactivo")

    if region_ids and role.name != "health_staff":
        raise UserValidationError("Solo los usuarios health_staff pueden tener region_ids asignadas")
