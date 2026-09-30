from .claim_create_service import create
from .claim_delete_service import delete
from .claim_get_all_service import get_all
from .claim_get_by_id_service import get_by_id
from .claim_update_service import update


class ClaimService:
    create = staticmethod(create)
    get_all = staticmethod(get_all)
    get_by_id = staticmethod(get_by_id)
    update = staticmethod(update)
    delete = staticmethod(delete)


claimService = ClaimService()
