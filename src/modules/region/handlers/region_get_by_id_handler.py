from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.regions_service import regionService


async def get_region_by_id_handler(region_id: str):
    try:
        region_uuid = parse_uuid(region_id, "region_id")
        region = await regionService.get_by_id(region_uuid)

        if region is None:
            return error(404, "Micro red no encontrada", ValueError(f"region_id={region_id}"))

        return success(200, "Micro red obtenida correctamente", region.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener la micro red", err)
