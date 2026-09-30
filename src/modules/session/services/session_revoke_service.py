from uuid import UUID

from ..repositories.session_repositories import sessionRepository


async def revoke(session_id: UUID, reason: str) -> str:
    return await sessionRepository.revoke(session_id, reason)


async def revoke_by_token(token_hash: str, reason: str) -> None:
    await sessionRepository.revoke_by_token(token_hash, reason)
