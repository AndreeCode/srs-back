from datetime import date

from ..domain.his_domain import HisChild
from ..repositories.his_repositories import hisRepository


async def find_child(document_number: str, birth_date: date | None = None) -> HisChild | None:
    document_number = document_number.strip()
    child = (await hisRepository.find_children([document_number])).get(document_number)

    if child is None or (birth_date is not None and child.birth_date != birth_date):
        return None

    return child
