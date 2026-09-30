from asyncpg.exceptions import ForeignKeyViolationError

from ....core.http.error import error


def foreign_key_violation_error(err: ForeignKeyViolationError):
    if err.constraint_name == "claims_service_id_fkey":
        return error(400, "El service_id indicado no existe", err)
    if err.constraint_name == "claims_health_facility_id_fkey":
        return error(400, "El health_facility_id indicado no existe", err)
    if err.constraint_name == "claims_child_id_fkey":
        return error(400, "El child_id indicado no existe", err)
    return error(400, "El usuario indicado no existe", err)
