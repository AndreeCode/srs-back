from uuid import UUID

from ..repositories.care_service_repositories import careServiceRepository


async def delete(care_service_id: UUID) -> str:
    return await careServiceRepository.delete(care_service_id)
