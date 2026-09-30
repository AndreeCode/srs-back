from uuid import UUID

from ..domain.care_service_domain import CareService
from ..repositories.care_service_repositories import careServiceRepository


async def get_all(package_id: UUID | None) -> list[CareService]:
    return await careServiceRepository.get_all(package_id)
