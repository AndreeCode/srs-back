from uuid import UUID

from ..repositories.child_repositories import childRepository


async def delete(child_id: UUID) -> str:
    return await childRepository.delete(child_id)
