from uuid import UUID

from ..domain.child_control_domain import ChildControl
from ..repositories.child_control_repositories import childControlRepository


async def get_by_id(child_control_id: UUID) -> ChildControl | None:
    return await childControlRepository.get_by_id(child_control_id)
