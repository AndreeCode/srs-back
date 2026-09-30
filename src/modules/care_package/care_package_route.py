from fastapi import APIRouter, Depends

from ...core.security.permission_guard import require_permission
from .handlers.care_package_create_handler import CarePackageCreateRequest
from .handlers.care_package_handlers import carePackageHandler
from .handlers.care_package_update_handler import CarePackageUpdateRequest

router = APIRouter(prefix="/care-packages", tags=["care-packages"])


@router.post("", dependencies=[Depends(require_permission("care_package.post"))])
async def create_care_package(body: CarePackageCreateRequest):
    return await carePackageHandler.create(body)


@router.get("", dependencies=[Depends(require_permission("care_package.get"))])
async def get_all_care_packages():
    return await carePackageHandler.get_all()


@router.get("/{care_package_id}", dependencies=[Depends(require_permission("care_package.get"))])
async def get_care_package_by_id(care_package_id: str):
    return await carePackageHandler.get_by_id(care_package_id)


@router.put("/{care_package_id}", dependencies=[Depends(require_permission("care_package.put"))])
async def update_care_package(care_package_id: str, body: CarePackageUpdateRequest):
    return await carePackageHandler.update(care_package_id, body)


@router.delete("/{care_package_id}", dependencies=[Depends(require_permission("care_package.delete"))])
async def delete_care_package(care_package_id: str):
    return await carePackageHandler.delete(care_package_id)
