from uuid import UUID

from ..repositories.user_region_repositories import userRegionRepository


async def delete(user_id: UUID, region_id: UUID) -> str:
    return await userRegionRepository.delete(user_id, region_id)
