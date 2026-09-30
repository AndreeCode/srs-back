from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.sessions_service import sessionService


async def revoke_session_handler(session_id: str):
    try:
        session_uuid = parse_uuid(session_id, "session_id")
        result = await sessionService.revoke(session_uuid, "revoked_by_admin")

        if result == "not_found":
            return error(404, "Sesion no encontrada", ValueError(f"session_id={session_id}"))

        if result == "already_revoked":
            return success(200, "La sesion ya estaba cerrada")

        return success(200, "Sesion cerrada correctamente")

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al cerrar la sesion", err)
