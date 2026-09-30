from typing import Optional

from fastapi import APIRouter, Depends, Request

from ...core.security.permission_guard import require_permission
from .domain.claim_domain import ClaimStatus
from .handlers.claim_create_handler import ClaimCreateRequest
from .handlers.claim_handlers import claimHandler
from .handlers.claim_update_handler import ClaimUpdateRequest

router = APIRouter(prefix="/claims", tags=["claims"])


@router.post("", dependencies=[Depends(require_permission("claim.post"))])
async def create_claim(request: Request, body: ClaimCreateRequest):
    return await claimHandler.create(request, body)


@router.get("", dependencies=[Depends(require_permission("claim.get"))])
async def get_all_claims(
    child_id: str | None = None,
    requester_user_id: str | None = None,
    status: Optional[ClaimStatus] = None,
):
    return await claimHandler.get_all(child_id, requester_user_id, status)


@router.get("/{claim_id}", dependencies=[Depends(require_permission("claim.get"))])
async def get_claim_by_id(claim_id: str):
    return await claimHandler.get_by_id(claim_id)


@router.put("/{claim_id}", dependencies=[Depends(require_permission("claim.put"))])
async def update_claim(request: Request, claim_id: str, body: ClaimUpdateRequest):
    return await claimHandler.update(request, claim_id, body)


@router.delete("/{claim_id}", dependencies=[Depends(require_permission("claim.delete"))])
async def delete_claim(claim_id: str):
    return await claimHandler.delete(claim_id)
