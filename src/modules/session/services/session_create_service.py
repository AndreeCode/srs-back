from ..domain.session_domain import Session
from ..repositories.session_repositories import sessionRepository


async def create(session: Session) -> Session:
    return await sessionRepository.create(session)
