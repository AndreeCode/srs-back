from uuid import UUID

from ..domain.device_domain import Device
from ..repositories.device_repositories import deviceRepository


async def get_by_id(device_id: UUID) -> Device | None:
    return await deviceRepository.get_by_id(device_id)
