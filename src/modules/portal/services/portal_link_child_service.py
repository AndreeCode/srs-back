from datetime import date
from uuid import UUID

from ...guardian.services.guardians_service import guardianService
from .portal_access_service import get_guardian


async def link_child(user_id: UUID, identifier: str, birth_date: date, relationship: str, ip: str | None = None) -> dict:
    guardian = await get_guardian(user_id)
    return await guardianService.link_child_self_service(guardian, identifier, birth_date, relationship, ip)
