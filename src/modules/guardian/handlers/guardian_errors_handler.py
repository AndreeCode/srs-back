from asyncpg.exceptions import UniqueViolationError

from ....core.http.error import error


def unique_violation_error(err: UniqueViolationError):
    if err.constraint_name == "guardians_user_id_key":
        return error(409, "El usuario indicado ya esta vinculado a otro apoderado", err)
    return error(409, "Ya existe un apoderado con ese DNI", err)
