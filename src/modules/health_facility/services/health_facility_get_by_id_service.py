from uuid import UUID

from ..domain.health_facility_domain import HealthFacility
from ..repositories.health_facility_repositories import healthFacilityRepository


async def get_by_id(health_facility_id: UUID) -> HealthFacility | None:
    return await healthFacilityRepository.get_by_id(health_facility_id)
