from ..domain.region_domain import Region
from ..repositories.region_repositories import regionRepository


async def create(region: Region) -> Region:
    return await regionRepository.create(region)
