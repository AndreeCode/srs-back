from fastapi import APIRouter, Depends, File, Form, UploadFile

from ...core.security.permission_guard import require_permission
from ...core.security.throttle import throttle
from .handlers.claim_evidence_handlers import claimEvidenceHandler

router = APIRouter(prefix="/claim-evidences", tags=["claim-evidences"])


@router.post("", dependencies=[Depends(require_permission("claim_evidence.post")), Depends(throttle("create_claim_evidence", 30, 600))])
async def create_claim_evidence(claim_id: str = Form(...), file: UploadFile = File(...)):
    return await claimEvidenceHandler.create(claim_id, file)


@router.get("", dependencies=[Depends(require_permission("claim_evidence.get"))])
async def get_all_claim_evidences(claim_id: str | None = None):
    return await claimEvidenceHandler.get_all(claim_id)


@router.get("/{claim_evidence_id}", dependencies=[Depends(require_permission("claim_evidence.get"))])
async def get_claim_evidence_by_id(claim_evidence_id: str):
    return await claimEvidenceHandler.get_by_id(claim_evidence_id)


@router.get("/{claim_evidence_id}/file", dependencies=[Depends(require_permission("claim_evidence.get")), Depends(throttle("download_claim_evidence", 60, 600))])
async def download_claim_evidence(claim_evidence_id: str):
    return await claimEvidenceHandler.download(claim_evidence_id)


@router.delete("/{claim_evidence_id}", dependencies=[Depends(require_permission("claim_evidence.delete"))])
async def delete_claim_evidence(claim_evidence_id: str):
    return await claimEvidenceHandler.delete(claim_evidence_id)
