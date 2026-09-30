from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.care_services_service import careServiceService


async def get_care_service_by_id_handler(care_service_id: str):
    try:
        care_service_uuid = parse_uuid(care_service_id, "care_service_id")
        care_service = await careServiceService.get_by_id(care_service_uuid)

        if care_service is None:
            return error(404, "Prestacion no encontrada", ValueError(f"care_service_id={care_service_id}"))

        return success(200, "Prestacion obtenida correctamente", care_service.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener la prestacion", err)
