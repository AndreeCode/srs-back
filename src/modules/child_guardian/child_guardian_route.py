from fastapi import APIRouter, Depends

from ...core.security.permission_guard import require_permission
from .handlers.child_guardian_create_handler import ChildGuardianCreateRequest
from .handlers.child_guardian_handlers import childGuardianHandler
from .handlers.child_guardian_update_handler import ChildGuardianUpdateRequest

router = APIRouter(prefix="/child-guardians", tags=["child-guardians"])


@router.post("", dependencies=[Depends(require_permission("child_guardian.post"))])
async def create_child_guardian(body: ChildGuardianCreateRequest):
    return await childGuardianHandler.create(body)


@router.get("", dependencies=[Depends(require_permission("child_guardian.get"))])
async def get_all_child_guardians(child_id: str | None = None, guardian_id: str | None = None):
    return await childGuardianHandler.get_all(child_id, guardian_id)


@router.get("/{child_id}/{guardian_id}", dependencies=[Depends(require_permission("child_guardian.get"))])
async def get_child_guardian_by_id(child_id: str, guardian_id: str):
    return await childGuardianHandler.get_by_id(child_id, guardian_id)


@router.put("/{child_id}/{guardian_id}", dependencies=[Depends(require_permission("child_guardian.put"))])
async def update_child_guardian(child_id: str, guardian_id: str, body: ChildGuardianUpdateRequest):
    return await childGuardianHandler.update(child_id, guardian_id, body)


@router.delete("/{child_id}/{guardian_id}", dependencies=[Depends(require_permission("child_guardian.delete"))])
async def delete_child_guardian(child_id: str, guardian_id: str):
    return await childGuardianHandler.delete(child_id, guardian_id)
