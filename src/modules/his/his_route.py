from fastapi import APIRouter, Depends

from ...core.security.permission_guard import require_permission
from .handlers.his_handlers import child_handler, guardian_handler

router = APIRouter(prefix="/his", tags=["his"])


@router.get("/children/{document_number}", dependencies=[Depends(require_permission("his.get"))])
async def get_his_child(document_number: str):
    return await child_handler(document_number)


@router.get("/guardians/{guardian_id}", dependencies=[Depends(require_permission("his.get"))])
async def get_his_children_of_guardian(guardian_id: str):
    return await guardian_handler(guardian_id)
