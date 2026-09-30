from fastapi import APIRouter, Depends, File, Form, Request, UploadFile

from ...core.security.permission_guard import require_permission
from .handlers.portal_claims_handler import PortalClaimCreateRequest
from .handlers.portal_handlers import portalHandler

router = APIRouter(prefix="/portal", tags=["portal"])


@router.get("", dependencies=[Depends(require_permission("portal.get"))])
async def get_portal(request: Request):
    return await portalHandler.overview(request)


@router.get("/claims", dependencies=[Depends(require_permission("portal.get"))])
async def get_portal_claims(request: Request):
    return await portalHandler.claims(request)


@router.post("/claims", dependencies=[Depends(require_permission("portal.post"))])
async def create_portal_claim(request: Request, body: PortalClaimCreateRequest):
    return await portalHandler.create_claim(request, body)


@router.post("/claim-evidences", dependencies=[Depends(require_permission("portal.post"))])
async def upload_portal_evidence(request: Request, claim_id: str = Form(...), file: UploadFile = File(...)):
    return await portalHandler.upload_evidence(request, claim_id, file)


@router.get("/claim-evidences/{claim_evidence_id}/file", dependencies=[Depends(require_permission("portal.get"))])
async def download_portal_evidence(request: Request, claim_evidence_id: str):
    return await portalHandler.download_evidence(request, claim_evidence_id)
