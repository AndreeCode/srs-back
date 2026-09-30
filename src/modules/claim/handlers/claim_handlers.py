from .claim_create_handler import create_claim_handler
from .claim_delete_handler import delete_claim_handler
from .claim_get_all_handler import get_all_claims_handler
from .claim_get_by_id_handler import get_claim_by_id_handler
from .claim_update_handler import update_claim_handler


class ClaimHandler:
    create = staticmethod(create_claim_handler)
    get_all = staticmethod(get_all_claims_handler)
    get_by_id = staticmethod(get_claim_by_id_handler)
    update = staticmethod(update_claim_handler)
    delete = staticmethod(delete_claim_handler)


claimHandler = ClaimHandler()
