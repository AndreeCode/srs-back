from uuid import UUID

from ..domain.user_domain import User
from ..repositories.user_repositories import userRepository


async def get_by_id(user_id: UUID) -> User | None:
    return await userRepository.get_by_id(user_id)
