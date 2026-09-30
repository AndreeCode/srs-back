from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError

from ....core.http.error import error


def unique_violation_error(err: UniqueViolationError):
    if err.constraint_name == "uq_children_dni":
        return error(409, "Ya existe un nino con ese DNI", err)
    return error(409, "Ya existe un nino con ese codigo de padron", err)


def foreign_key_violation_error(err: ForeignKeyViolationError):
    if err.constraint_name == "children_registered_by_fkey":
        return error(400, "El usuario que registra no existe", err)
    return error(400, "El health_facility_id indicado no existe", err)
