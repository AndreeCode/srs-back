from fastapi import APIRouter, Depends

from ...core.security.permission_guard import require_permission
from .handlers.guardian_create_handler import GuardianCreateRequest
from .handlers.guardian_handlers import guardianHandler
from .handlers.guardian_update_handler import GuardianUpdateRequest

router = APIRouter(prefix="/guardians", tags=["guardians"])


@router.post("", dependencies=[Depends(require_permission("guardian.post"))])
async def create_guardian(body: GuardianCreateRequest):
    return await guardianHandler.create(body)


@router.get("", dependencies=[Depends(require_permission("guardian.get"))])
async def get_all_guardians():
    return await guardianHandler.get_all()


@router.get("/{guardian_id}", dependencies=[Depends(require_permission("guardian.get"))])
async def get_guardian_by_id(guardian_id: str):
    return await guardianHandler.get_by_id(guardian_id)


@router.put("/{guardian_id}", dependencies=[Depends(require_permission("guardian.put"))])
async def update_guardian(guardian_id: str, body: GuardianUpdateRequest):
    return await guardianHandler.update(guardian_id, body)


@router.delete("/{guardian_id}", dependencies=[Depends(require_permission("guardian.delete"))])
async def delete_guardian(guardian_id: str):
    return await guardianHandler.delete(guardian_id)
