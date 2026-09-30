from .claim_create_repository import create_claim
from .claim_delete_repository import delete_claim
from .claim_get_all_repository import get_all_claims
from .claim_get_by_id_repository import get_claim_by_id
from .claim_update_repository import update_claim


class ClaimRepository:
    create = staticmethod(create_claim)
    get_all = staticmethod(get_all_claims)
    get_by_id = staticmethod(get_claim_by_id)
    update = staticmethod(update_claim)
    delete = staticmethod(delete_claim)


claimRepository = ClaimRepository()
