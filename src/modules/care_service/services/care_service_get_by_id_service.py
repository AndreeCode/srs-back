from uuid import UUID

from ..domain.care_service_domain import CareService
from ..repositories.care_service_repositories import careServiceRepository


async def get_by_id(care_service_id: UUID) -> CareService | None:
    return await careServiceRepository.get_by_id(care_service_id)
