from uuid import UUID

from ..domain.user_region_domain import UserRegion
from ..repositories.user_region_repositories import userRegionRepository


async def get_by_id(user_id: UUID, region_id: UUID) -> UserRegion | None:
    return await userRegionRepository.get_by_id(user_id, region_id)
