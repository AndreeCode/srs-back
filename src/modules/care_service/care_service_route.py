from fastapi import APIRouter, Depends

from ...core.security.permission_guard import require_permission
from .handlers.care_service_create_handler import CareServiceCreateRequest
from .handlers.care_service_handlers import careServiceHandler
from .handlers.care_service_update_handler import CareServiceUpdateRequest

router = APIRouter(prefix="/care-services", tags=["care-services"])


@router.post("", dependencies=[Depends(require_permission("care_service.post"))])
async def create_care_service(body: CareServiceCreateRequest):
    return await careServiceHandler.create(body)


@router.get("", dependencies=[Depends(require_permission("care_service.get"))])
async def get_all_care_services(package_id: str | None = None):
    return await careServiceHandler.get_all(package_id)


@router.get("/{care_service_id}", dependencies=[Depends(require_permission("care_service.get"))])
async def get_care_service_by_id(care_service_id: str):
    return await careServiceHandler.get_by_id(care_service_id)


@router.put("/{care_service_id}", dependencies=[Depends(require_permission("care_service.put"))])
async def update_care_service(care_service_id: str, body: CareServiceUpdateRequest):
    return await careServiceHandler.update(care_service_id, body)


@router.delete("/{care_service_id}", dependencies=[Depends(require_permission("care_service.delete"))])
async def delete_care_service(care_service_id: str):
    return await careServiceHandler.delete(care_service_id)
