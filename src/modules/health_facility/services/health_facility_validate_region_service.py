from uuid import UUID

from ...region.services.regions_service import regionService
from ..domain.health_facility_errors import HealthFacilityValidationError


async def validate_region(region_id: UUID) -> None:
    region = await regionService.get_by_id(region_id)

    if region is None:
        raise HealthFacilityValidationError("El region_id indicado no existe")

    if not region.active:
        raise HealthFacilityValidationError("La micro red indicada esta inactiva")
