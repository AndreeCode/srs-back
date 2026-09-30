from ..domain.session_domain import Session
from ..repositories.session_repositories import sessionRepository


async def get_active_by_token(token_hash: str) -> Session | None:
    return await sessionRepository.get_active_by_token(token_hash)
