from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.user_regions_service import userRegionService


async def get_user_region_by_id_handler(user_id: str, region_id: str):
    try:
        user_uuid = parse_uuid(user_id, "user_id")
        region_uuid = parse_uuid(region_id, "region_id")
        user_region = await userRegionService.get_by_id(user_uuid, region_uuid)

        if user_region is None:
            return error(404, "Asignacion no encontrada", ValueError(f"user_id={user_id} region_id={region_id}"))

        return success(200, "Asignacion obtenida correctamente", user_region.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener la asignacion", err)
