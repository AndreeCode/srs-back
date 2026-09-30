from uuid import UUID

from ..repositories.user_repositories import userRepository


async def delete(user_id: UUID) -> str:
    return await userRepository.delete(user_id)
