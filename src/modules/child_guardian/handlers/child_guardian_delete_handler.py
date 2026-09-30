from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.child_guardians_service import childGuardianService


async def delete_child_guardian_handler(child_id: str, guardian_id: str):
    try:
        child_uuid = parse_uuid(child_id, "child_id")
        guardian_uuid = parse_uuid(guardian_id, "guardian_id")
        result = await childGuardianService.delete(child_uuid, guardian_uuid)

        if result == "not_found":
            return error(404, "Vinculo no encontrado", ValueError(f"child_id={child_id} guardian_id={guardian_id}"))

        return success(200, "Apoderado desvinculado del nino correctamente")

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al desvincular el apoderado", err)
