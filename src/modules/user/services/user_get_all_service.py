from ..domain.user_domain import User
from ..repositories.user_repositories import userRepository


async def get_all() -> list[User]:
    return await userRepository.get_all()
