from fastapi import APIRouter, Depends

from ...core.security.permission_guard import require_permission
from .handlers.device_handlers import deviceHandler
from .handlers.device_update_handler import DeviceUpdateRequest

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("", dependencies=[Depends(require_permission("device.get"))])
async def get_all_devices(user_id: str | None = None):
    return await deviceHandler.get_all(user_id)


@router.get("/{device_id}", dependencies=[Depends(require_permission("device.get"))])
async def get_device_by_id(device_id: str):
    return await deviceHandler.get_by_id(device_id)


@router.put("/{device_id}", dependencies=[Depends(require_permission("device.put"))])
async def update_device(device_id: str, body: DeviceUpdateRequest):
    return await deviceHandler.update(device_id, body)
