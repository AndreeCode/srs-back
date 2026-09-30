from ..domain.region_domain import Region
from ..repositories.region_repositories import regionRepository


async def update(region: Region) -> Region | None:
    return await regionRepository.update(region)
