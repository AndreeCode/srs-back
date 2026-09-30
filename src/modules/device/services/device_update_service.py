from uuid import UUID

from ..domain.device_domain import BlockScope, Device
from ..repositories.device_repositories import deviceRepository


async def update(device_id: UUID, trusted: bool, reason: str | None = None, scope: BlockScope = "account") -> Device | None:
    return await deviceRepository.update(device_id, trusted, reason, scope)
