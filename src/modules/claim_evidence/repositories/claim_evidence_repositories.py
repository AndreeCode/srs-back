from .claim_evidence_count_repository import count_claim_evidences
from .claim_evidence_create_repository import create_claim_evidence
from .claim_evidence_delete_repository import delete_claim_evidence
from .claim_evidence_get_all_repository import get_all_claim_evidences
from .claim_evidence_get_by_id_repository import get_claim_evidence_by_id


class ClaimEvidenceRepository:
    create = staticmethod(create_claim_evidence)
    get_all = staticmethod(get_all_claim_evidences)
    get_by_id = staticmethod(get_claim_evidence_by_id)
    count = staticmethod(count_claim_evidences)
    delete = staticmethod(delete_claim_evidence)


claimEvidenceRepository = ClaimEvidenceRepository()
