from typing import Optional

from fastapi import APIRouter, Depends, Request

from ...core.security.permission_guard import require_permission
from .domain.child_control_domain import ControlStatus
from .handlers.child_control_create_handler import ChildControlCreateRequest
from .handlers.child_control_handlers import childControlHandler
from .handlers.child_control_update_handler import ChildControlUpdateRequest

router = APIRouter(prefix="/child-controls", tags=["child-controls"])


@router.post("", dependencies=[Depends(require_permission("child_control.post"))])
async def create_child_control(request: Request, body: ChildControlCreateRequest):
    return await childControlHandler.create(request, body)


@router.get("", dependencies=[Depends(require_permission("child_control.get"))])
async def get_all_child_controls(
    child_id: str | None = None,
    service_id: str | None = None,
    status: Optional[ControlStatus] = None,
):
    return await childControlHandler.get_all(child_id, service_id, status)


@router.get("/{child_control_id}", dependencies=[Depends(require_permission("child_control.get"))])
async def get_child_control_by_id(child_control_id: str):
    return await childControlHandler.get_by_id(child_control_id)


@router.put("/{child_control_id}", dependencies=[Depends(require_permission("child_control.put"))])
async def update_child_control(child_control_id: str, body: ChildControlUpdateRequest):
    return await childControlHandler.update(child_control_id, body)


@router.delete("/{child_control_id}", dependencies=[Depends(require_permission("child_control.delete"))])
async def delete_child_control(child_control_id: str):
    return await childControlHandler.delete(child_control_id)
