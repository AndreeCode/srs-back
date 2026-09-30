from uuid import UUID

from ..domain.health_facility_domain import HealthFacility
from ..repositories.health_facility_repositories import healthFacilityRepository


async def get_all(region_id: UUID | None) -> list[HealthFacility]:
    return await healthFacilityRepository.get_all(region_id)
