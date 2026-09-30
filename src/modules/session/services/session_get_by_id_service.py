from uuid import UUID

from ..domain.session_domain import Session
from ..repositories.session_repositories import sessionRepository


async def get_by_id(session_id: UUID) -> Session | None:
    return await sessionRepository.get_by_id(session_id)
