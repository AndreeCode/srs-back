from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.care_services_service import careServiceService


async def delete_care_service_handler(care_service_id: str):
    try:
        care_service_uuid = parse_uuid(care_service_id, "care_service_id")
        result = await careServiceService.delete(care_service_uuid)

        if result == "not_found":
            return error(404, "Prestacion no encontrada", ValueError(f"care_service_id={care_service_id}"))

        if result == "deleted":
            return success(200, "Prestacion eliminada correctamente")

        return success(200, "Prestacion desactivada porque tiene controles o reclamos registrados")

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al eliminar la prestacion", err)
