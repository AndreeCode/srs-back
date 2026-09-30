from uuid import UUID

from ..repositories.child_control_repositories import childControlRepository


async def delete(child_control_id: UUID) -> str:
    return await childControlRepository.delete(child_control_id)
