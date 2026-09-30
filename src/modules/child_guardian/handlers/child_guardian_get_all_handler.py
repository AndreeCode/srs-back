from ....core.http.error import error
from ....core.http.list import list_response
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.child_guardians_service import childGuardianService


async def get_all_child_guardians_handler(child_id: str | None, guardian_id: str | None):
    try:
        child_uuid = parse_uuid(child_id, "child_id") if child_id is not None else None
        guardian_uuid = parse_uuid(guardian_id, "guardian_id") if guardian_id is not None else None

        child_guardians = await childGuardianService.get_all(child_uuid, guardian_uuid)
        data = [child_guardian.to_dict() for child_guardian in child_guardians]
        return list_response(200, "Vinculos obtenidos correctamente", data, {"count": len(data)})

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener los vinculos", err)
