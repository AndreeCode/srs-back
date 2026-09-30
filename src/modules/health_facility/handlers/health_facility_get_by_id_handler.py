from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.health_facilities_service import healthFacilityService


async def get_health_facility_by_id_handler(health_facility_id: str):
    try:
        health_facility_uuid = parse_uuid(health_facility_id, "health_facility_id")
        health_facility = await healthFacilityService.get_by_id(health_facility_uuid)

        if health_facility is None:
            return error(404, "Establecimiento no encontrado", ValueError(f"health_facility_id={health_facility_id}"))

        return success(200, "Establecimiento obtenido correctamente", health_facility.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener el establecimiento", err)
