from .claim_evidence_create_service import create
from .claim_evidence_delete_service import delete
from .claim_evidence_get_all_service import get_all
from .claim_evidence_get_by_id_service import get_by_id


class ClaimEvidenceService:
    create = staticmethod(create)
    get_all = staticmethod(get_all)
    get_by_id = staticmethod(get_by_id)
    delete = staticmethod(delete)


claimEvidenceService = ClaimEvidenceService()
