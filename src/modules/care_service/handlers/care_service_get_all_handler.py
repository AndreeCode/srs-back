from ....core.http.error import error
from ....core.http.list import list_response
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.care_services_service import careServiceService


async def get_all_care_services_handler(package_id: str | None):
    try:
        package_uuid = parse_uuid(package_id, "package_id") if package_id is not None else None

        care_services = await careServiceService.get_all(package_uuid)
        data = [care_service.to_dict() for care_service in care_services]
        return list_response(200, "Prestaciones obtenidas correctamente", data, {"count": len(data)})

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener las prestaciones", err)
