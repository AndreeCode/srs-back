from uuid import UUID

from ..domain.child_control_domain import ChildControl
from ..repositories.child_control_repositories import childControlRepository


async def get_all(child_id: UUID | None, service_id: UUID | None, status: str | None) -> list[ChildControl]:
    return await childControlRepository.get_all(child_id, service_id, status)
