from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ...core.security.permission_guard import require_permission
from .handlers.his_handlers import child_handler, guardian_handler

router = APIRouter(prefix="/his", tags=["his"])


class HisChildLookupRequest(BaseModel):
    document_number: str = Field(min_length=1, max_length=15)


@router.post("/children/lookup", dependencies=[Depends(require_permission("his.get"))])
async def lookup_his_child(body: HisChildLookupRequest):
    return await child_handler(body.document_number)


@router.get("/children/{document_number}", dependencies=[Depends(require_permission("his.get"))])
async def get_his_child(document_number: str):
    return await child_handler(document_number)


@router.get("/guardians/{guardian_id}", dependencies=[Depends(require_permission("his.get"))])
async def get_his_children_of_guardian(guardian_id: str):
    return await guardian_handler(guardian_id)
