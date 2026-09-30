from asyncpg.exceptions import CheckViolationError, ForeignKeyViolationError

from ....core.http.error import error


def foreign_key_violation_error(err: ForeignKeyViolationError):
    if err.constraint_name == "child_controls_service_id_fkey":
        return error(400, "El service_id indicado no existe", err)
    if err.constraint_name == "child_controls_health_facility_id_fkey":
        return error(400, "El health_facility_id indicado no existe", err)
    if err.constraint_name == "child_controls_registered_by_fkey":
        return error(400, "El usuario que registra no existe", err)
    return error(400, "El child_id indicado no existe", err)


def check_violation_error(err: CheckViolationError):
    return error(400, "Fechas o estado del control invalidos", err)
