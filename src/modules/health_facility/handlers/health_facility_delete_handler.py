from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.health_facilities_service import healthFacilityService


async def delete_health_facility_handler(health_facility_id: str):
    try:
        health_facility_uuid = parse_uuid(health_facility_id, "health_facility_id")
        result = await healthFacilityService.delete(health_facility_uuid)

        if result == "not_found":
            return error(404, "Establecimiento no encontrado", ValueError(f"health_facility_id={health_facility_id}"))

        if result == "deleted":
            return success(200, "Establecimiento eliminado correctamente")

        return success(200, "Establecimiento desactivado porque tiene ninos registrados")

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al eliminar el establecimiento", err)
