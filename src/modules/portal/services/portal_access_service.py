from uuid import UUID

from ...claim.domain.claim_domain import Claim
from ...claim.services.claims_service import claimService
from ...guardian.domain.guardian_domain import Guardian
from ..domain.portal_errors import PortalAccessError, PortalNotFoundError
from ..repositories.portal_repositories import portalRepository


async def get_guardian(user_id: UUID) -> Guardian:
    guardian = await portalRepository.get_guardian_by_user(user_id)

    if guardian is None:
        raise PortalAccessError("Tu cuenta no está vinculada a ningún padre o apoderado")

    return guardian


async def get_child_ids(guardian: Guardian) -> set[UUID]:
    return {child.id for child, _ in await portalRepository.get_children_of_guardian(guardian.id)}


async def ensure_own_child(user_id: UUID, child_id: UUID) -> Guardian:
    guardian = await get_guardian(user_id)

    if child_id not in await get_child_ids(guardian):
        raise PortalAccessError("Solo puedes consultar a tus propios hijos")

    return guardian


async def ensure_own_claim(user_id: UUID, claim_id: UUID) -> Claim:
    claim = await claimService.get_by_id(claim_id)

    if claim is None or claim.requester_user_id != user_id:
        raise PortalNotFoundError("Reclamo no encontrado")

    return claim
