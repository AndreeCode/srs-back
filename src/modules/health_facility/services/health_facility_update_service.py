from ..domain.health_facility_domain import HealthFacility
from ..repositories.health_facility_repositories import healthFacilityRepository
from .health_facility_validate_region_service import validate_region


async def update(health_facility: HealthFacility, current: HealthFacility) -> HealthFacility | None:
    if health_facility.region_id != current.region_id:
        await validate_region(health_facility.region_id)

    return await healthFacilityRepository.update(health_facility)
