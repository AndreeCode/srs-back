from ...region.services.regions_service import regionService
from ...role.services.roles_service import roleService
from ...user.services.users_service import userService
from ..domain.user_region_domain import UserRegion
from ..domain.user_region_errors import UserRegionValidationError
from ..repositories.user_region_repositories import userRegionRepository


async def create(user_region: UserRegion) -> UserRegion:
    user = await userService.get_by_id(user_region.user_id)

    if user is None:
        raise UserRegionValidationError("El user_id indicado no existe")

    role = await roleService.get_by_id(user.role_id)

    if role is None or role.name != "health_staff":
        raise UserRegionValidationError("Solo los usuarios health_staff pueden tener micro redes asignadas")

    region = await regionService.get_by_id(user_region.region_id)

    if region is None:
        raise UserRegionValidationError("El region_id indicado no existe")

    if not region.active:
        raise UserRegionValidationError("La micro red indicada esta inactiva")

    return await userRegionRepository.create(user_region)
