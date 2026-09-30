from fastapi import APIRouter, Depends

from ...core.security.permission_guard import require_permission
from .handlers.user_region_create_handler import UserRegionCreateRequest
from .handlers.user_region_handlers import userRegionHandler

router = APIRouter(prefix="/user-regions", tags=["user-regions"])


@router.post("", dependencies=[Depends(require_permission("user_region.post"))])
async def create_user_region(body: UserRegionCreateRequest):
    return await userRegionHandler.create(body)


@router.get("", dependencies=[Depends(require_permission("user_region.get"))])
async def get_all_user_regions(user_id: str | None = None, region_id: str | None = None):
    return await userRegionHandler.get_all(user_id, region_id)


@router.get("/{user_id}/{region_id}", dependencies=[Depends(require_permission("user_region.get"))])
async def get_user_region_by_id(user_id: str, region_id: str):
    return await userRegionHandler.get_by_id(user_id, region_id)


@router.delete("/{user_id}/{region_id}", dependencies=[Depends(require_permission("user_region.delete"))])
async def delete_user_region(user_id: str, region_id: str):
    return await userRegionHandler.delete(user_id, region_id)
