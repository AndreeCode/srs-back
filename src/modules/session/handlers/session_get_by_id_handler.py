from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.sessions_service import sessionService


async def get_session_by_id_handler(session_id: str):
    try:
        session_uuid = parse_uuid(session_id, "session_id")
        session = await sessionService.get_by_id(session_uuid)

        if session is None:
            return error(404, "Sesion no encontrada", ValueError(f"session_id={session_id}"))

        return success(200, "Sesion obtenida correctamente", session.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener la sesion", err)
