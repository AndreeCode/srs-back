from fastapi import APIRouter, Depends

from ...core.security.permission_guard import require_permission
from .handlers.health_facility_create_handler import HealthFacilityCreateRequest
from .handlers.health_facility_handlers import healthFacilityHandler
from .handlers.health_facility_update_handler import HealthFacilityUpdateRequest

router = APIRouter(prefix="/health-facilities", tags=["health-facilities"])


@router.post("", dependencies=[Depends(require_permission("health_facility.post"))])
async def create_health_facility(body: HealthFacilityCreateRequest):
    return await healthFacilityHandler.create(body)


@router.get("", dependencies=[Depends(require_permission("health_facility.get"))])
async def get_all_health_facilities(region_id: str | None = None):
    return await healthFacilityHandler.get_all(region_id)


@router.get("/{health_facility_id}", dependencies=[Depends(require_permission("health_facility.get"))])
async def get_health_facility_by_id(health_facility_id: str):
    return await healthFacilityHandler.get_by_id(health_facility_id)


@router.put("/{health_facility_id}", dependencies=[Depends(require_permission("health_facility.put"))])
async def update_health_facility(health_facility_id: str, body: HealthFacilityUpdateRequest):
    return await healthFacilityHandler.update(health_facility_id, body)


@router.delete("/{health_facility_id}", dependencies=[Depends(require_permission("health_facility.delete"))])
async def delete_health_facility(health_facility_id: str):
    return await healthFacilityHandler.delete(health_facility_id)
