from ....core.http.error import error
from ....core.http.list import list_response
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.user_regions_service import userRegionService


async def get_all_user_regions_handler(user_id: str | None, region_id: str | None):
    try:
        user_uuid = parse_uuid(user_id, "user_id") if user_id is not None else None
        region_uuid = parse_uuid(region_id, "region_id") if region_id is not None else None

        user_regions = await userRegionService.get_all(user_uuid, region_uuid)
        data = [user_region.to_dict() for user_region in user_regions]
        return list_response(200, "Asignaciones obtenidas correctamente", data, {"count": len(data)})

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener las asignaciones", err)
