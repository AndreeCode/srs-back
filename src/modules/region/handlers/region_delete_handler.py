from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.regions_service import regionService


async def delete_region_handler(region_id: str):
    try:
        region_uuid = parse_uuid(region_id, "region_id")
        result = await regionService.delete(region_uuid)

        if result == "not_found":
            return error(404, "Micro red no encontrada", ValueError(f"region_id={region_id}"))

        if result == "deleted":
            return success(200, "Micro red eliminada correctamente")

        return success(200, "Micro red desactivada porque tiene establecimientos o usuarios asignados")

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al eliminar la micro red", err)
