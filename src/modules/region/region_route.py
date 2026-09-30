from fastapi import APIRouter, Depends

from ...core.security.permission_guard import require_permission
from .handlers.region_create_handler import RegionCreateRequest
from .handlers.region_handlers import regionHandler
from .handlers.region_update_handler import RegionUpdateRequest

router = APIRouter(prefix="/regions", tags=["regions"])


@router.post("", dependencies=[Depends(require_permission("region.post"))])
async def create_region(body: RegionCreateRequest):
    return await regionHandler.create(body)


@router.get("", dependencies=[Depends(require_permission("region.get"))])
async def get_all_regions():
    return await regionHandler.get_all()


@router.get("/{region_id}", dependencies=[Depends(require_permission("region.get"))])
async def get_region_by_id(region_id: str):
    return await regionHandler.get_by_id(region_id)


@router.put("/{region_id}", dependencies=[Depends(require_permission("region.put"))])
async def update_region(region_id: str, body: RegionUpdateRequest):
    return await regionHandler.update(region_id, body)


@router.delete("/{region_id}", dependencies=[Depends(require_permission("region.delete"))])
async def delete_region(region_id: str):
    return await regionHandler.delete(region_id)
