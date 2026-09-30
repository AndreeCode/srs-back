from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.audit_logs_service import auditLogService


async def get_audit_log_by_id_handler(audit_log_id: str):
    try:
        audit_log_uuid = parse_uuid(audit_log_id, "audit_log_id")
        audit_log = await auditLogService.get_by_id(audit_log_uuid)

        if audit_log is None:
            return error(404, "Registro de auditoria no encontrado", ValueError(f"audit_log_id={audit_log_id}"))

        return success(200, "Registro de auditoria obtenido correctamente", audit_log.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener el registro de auditoria", err)
