from uuid import UUID

from ..repositories.health_facility_repositories import healthFacilityRepository


async def delete(health_facility_id: UUID) -> str:
    return await healthFacilityRepository.delete(health_facility_id)
