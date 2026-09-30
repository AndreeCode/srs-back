from fastapi import APIRouter, Depends

from ...core.security.permission_guard import require_permission
from .handlers.role_create_handler import RoleCreateRequest
from .handlers.role_handlers import roleHandler
from .handlers.role_update_handler import RoleUpdateRequest

router = APIRouter(prefix="/roles", tags=["roles"])


@router.post("", dependencies=[Depends(require_permission("role.post"))])
async def create_role(body: RoleCreateRequest):
    return await roleHandler.create(body)


@router.get("", dependencies=[Depends(require_permission("role.get"))])
async def get_all_roles():
    return await roleHandler.get_all()


@router.get("/{role_id}", dependencies=[Depends(require_permission("role.get"))])
async def get_role_by_id(role_id: str):
    return await roleHandler.get_by_id(role_id)


@router.put("/{role_id}", dependencies=[Depends(require_permission("role.put"))])
async def update_role(role_id: str, body: RoleUpdateRequest):
    return await roleHandler.update(role_id, body)


@router.delete("/{role_id}", dependencies=[Depends(require_permission("role.delete"))])
async def delete_role(role_id: str):
    return await roleHandler.delete(role_id)
