from ....core.http.error import error
from ....core.http.list import list_response
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.health_facilities_service import healthFacilityService


async def get_all_health_facilities_handler(region_id: str | None):
    try:
        region_uuid = parse_uuid(region_id, "region_id") if region_id is not None else None

        health_facilities = await healthFacilityService.get_all(region_uuid)
        data = [health_facility.to_dict() for health_facility in health_facilities]
        return list_response(200, "Establecimientos obtenidos correctamente", data, {"count": len(data)})

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener los establecimientos", err)
