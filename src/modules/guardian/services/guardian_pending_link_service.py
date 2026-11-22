from uuid import UUID

from ..repositories.guardian_repositories import guardianRepository


async def get_pending_links() -> list[dict]:
    return await guardianRepository.get_pending_links()


async def approve_pending_link(source: str, guardian_id: UUID, child_key: str, verified_by: UUID) -> bool:
    return await guardianRepository.approve_pending_link(source, guardian_id, child_key, verified_by)


async def reject_pending_link(source: str, guardian_id: UUID, child_key: str) -> bool:
    return await guardianRepository.reject_pending_link(source, guardian_id, child_key)
