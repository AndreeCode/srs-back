from uuid import UUID

from ..repositories.region_repositories import regionRepository


async def delete(region_id: UUID) -> str:
    return await regionRepository.delete(region_id)
