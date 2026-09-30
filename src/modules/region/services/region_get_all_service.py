from ..domain.region_domain import Region
from ..repositories.region_repositories import regionRepository


async def get_all() -> list[Region]:
    return await regionRepository.get_all()
