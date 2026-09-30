from uuid import UUID

from ..domain.device_domain import Device
from ..repositories.device_repositories import deviceRepository


async def get_all(user_id: UUID | None) -> list[Device]:
    return await deviceRepository.get_all(user_id)
