from ..domain.child_domain import Child
from ..repositories.child_repositories import childRepository


async def get_all() -> list[Child]:
    return await childRepository.get_all()
