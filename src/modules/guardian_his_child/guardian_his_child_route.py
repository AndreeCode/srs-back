from fastapi import APIRouter, Depends, Request

from ...core.security.permission_guard import require_permission
from .handlers.guardian_his_child_handlers import (
    GuardianHisChildCreateRequest,
    GuardianHisChildUpdateRequest,
    guardianHisChildHandler,
)

router = APIRouter(prefix="/guardian-his-children", tags=["guardian-his-children"])


@router.post("", dependencies=[Depends(require_permission("guardian_his_child.post"))])
async def create_guardian_his_child(request: Request, body: GuardianHisChildCreateRequest):
    return await guardianHisChildHandler.create(request, body)


@router.get("", dependencies=[Depends(require_permission("guardian_his_child.get"))])
async def get_all_guardian_his_children(guardian_id: str | None = None, document_number: str | None = None):
    return await guardianHisChildHandler.get_all(guardian_id, document_number)


@router.put("/{guardian_id}/{document_number}", dependencies=[Depends(require_permission("guardian_his_child.put"))])
async def update_guardian_his_child(guardian_id: str, document_number: str, body: GuardianHisChildUpdateRequest):
    return await guardianHisChildHandler.update(guardian_id, document_number, body)


@router.delete("/{guardian_id}/{document_number}", dependencies=[Depends(require_permission("guardian_his_child.delete"))])
async def delete_guardian_his_child(guardian_id: str, document_number: str):
    return await guardianHisChildHandler.delete(guardian_id, document_number)
