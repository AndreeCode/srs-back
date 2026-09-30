from uuid import UUID

from ..domain.region_domain import Region
from ..repositories.region_repositories import regionRepository


async def get_by_id(region_id: UUID) -> Region | None:
    return await regionRepository.get_by_id(region_id)
