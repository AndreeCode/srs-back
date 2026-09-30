from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.guardians_service import guardianService


async def delete_guardian_handler(guardian_id: str):
    try:
        guardian_uuid = parse_uuid(guardian_id, "guardian_id")
        result = await guardianService.delete(guardian_uuid)

        if result == "not_found":
            return error(404, "Apoderado no encontrado", ValueError(f"guardian_id={guardian_id}"))

        return success(200, "Apoderado desactivado correctamente")

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al eliminar el apoderado", err)
