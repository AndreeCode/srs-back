from uuid import UUID

from ..domain.user_region_domain import UserRegion
from ..repositories.user_region_repositories import userRegionRepository


async def get_all(user_id: UUID | None, region_id: UUID | None) -> list[UserRegion]:
    return await userRegionRepository.get_all(user_id, region_id)
