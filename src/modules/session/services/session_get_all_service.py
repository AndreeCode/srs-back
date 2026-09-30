from uuid import UUID

from ..domain.session_domain import Session
from ..repositories.session_repositories import sessionRepository


async def get_all(user_id: UUID | None, device_id: UUID | None, active: bool | None) -> list[Session]:
    return await sessionRepository.get_all(user_id, device_id, active)
