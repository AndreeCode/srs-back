from uuid import UUID

from ....core.security.access_error import AccessDeniedError
from ..repositories.user_repositories import userRepository
from .user_access_service import ensure_can_manage


async def delete(caller_id: UUID, user_id: UUID) -> str:
    if caller_id == user_id:
        raise AccessDeniedError("No puedes desactivar tu propia cuenta")

    current = await userRepository.get_by_id(user_id)

    if current is None:
        return "not_found"

    await ensure_can_manage(caller_id, current)
    return await userRepository.delete(user_id)
