from ..domain.health_facility_domain import HealthFacility
from ..repositories.health_facility_repositories import healthFacilityRepository
from .health_facility_validate_region_service import validate_region


async def create(health_facility: HealthFacility) -> HealthFacility:
    await validate_region(health_facility.region_id)
    return await healthFacilityRepository.create(health_facility)
