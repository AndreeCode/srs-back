from fastapi import APIRouter, Depends, Request

from ...core.security.permission_guard import require_permission
from .handlers.child_create_handler import ChildCreateRequest
from .handlers.child_handlers import childHandler
from .handlers.child_update_handler import ChildUpdateRequest

router = APIRouter(prefix="/children", tags=["children"])


@router.post("", dependencies=[Depends(require_permission("child.post"))])
async def create_child(request: Request, body: ChildCreateRequest):
    return await childHandler.create(request, body)


@router.get("", dependencies=[Depends(require_permission("child.get"))])
async def get_all_children():
    return await childHandler.get_all()


@router.get("/{child_id}", dependencies=[Depends(require_permission("child.get"))])
async def get_child_by_id(child_id: str):
    return await childHandler.get_by_id(child_id)


@router.put("/{child_id}", dependencies=[Depends(require_permission("child.put"))])
async def update_child(child_id: str, body: ChildUpdateRequest):
    return await childHandler.update(child_id, body)


@router.delete("/{child_id}", dependencies=[Depends(require_permission("child.delete"))])
async def delete_child(child_id: str):
    return await childHandler.delete(child_id)
