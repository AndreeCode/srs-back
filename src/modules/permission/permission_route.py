from fastapi import APIRouter, Depends

from ...core.security.permission_guard import require_permission
from .handlers.permission_create_handler import PermissionCreateRequest
from .handlers.permission_handlers import permissionHandler
from .handlers.permission_update_handler import PermissionUpdateRequest

router = APIRouter(prefix="/permissions", tags=["permissions"])


@router.post("", dependencies=[Depends(require_permission("permission.post"))])
async def create_permission(body: PermissionCreateRequest):
    return await permissionHandler.create(body)


@router.get("", dependencies=[Depends(require_permission("permission.get"))])
async def get_all_permissions():
    return await permissionHandler.get_all()


@router.get("/{permission_id}", dependencies=[Depends(require_permission("permission.get"))])
async def get_permission_by_id(permission_id: str):
    return await permissionHandler.get_by_id(permission_id)


@router.put("/{permission_id}", dependencies=[Depends(require_permission("permission.put"))])
async def update_permission(permission_id: str, body: PermissionUpdateRequest):
    return await permissionHandler.update(permission_id, body)


@router.delete("/{permission_id}", dependencies=[Depends(require_permission("permission.delete"))])
async def delete_permission(permission_id: str):
    return await permissionHandler.delete(permission_id)
