from uuid import UUID

from ..domain.device_domain import Device
from ..repositories.device_repositories import deviceRepository


async def register(user_id: UUID, device_hash: str, user_agent: str | None) -> Device:
    return await deviceRepository.register(user_id, device_hash, user_agent)
