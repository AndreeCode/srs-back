from uuid import UUID


class InvalidUUIDError(ValueError):
    pass


def parse_uuid(value: str, field_name: str) -> UUID:
    try:
        return UUID(value)
    except ValueError:
        raise InvalidUUIDError(f"{field_name} debe ser un UUID valido: {value}")
