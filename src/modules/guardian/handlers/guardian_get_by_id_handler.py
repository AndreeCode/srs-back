from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.guardians_service import guardianService


async def get_guardian_by_id_handler(guardian_id: str):
    try:
        guardian_uuid = parse_uuid(guardian_id, "guardian_id")
        guardian = await guardianService.get_by_id(guardian_uuid)

        if guardian is None:
            return error(404, "Apoderado no encontrado", ValueError(f"guardian_id={guardian_id}"))

        return success(200, "Apoderado obtenido correctamente", guardian.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener el apoderado", err)
