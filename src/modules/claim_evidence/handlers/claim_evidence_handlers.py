from .claim_evidence_create_handler import create_claim_evidence_handler
from .claim_evidence_delete_handler import delete_claim_evidence_handler
from .claim_evidence_download_handler import download_claim_evidence_handler
from .claim_evidence_get_all_handler import get_all_claim_evidences_handler
from .claim_evidence_get_by_id_handler import get_claim_evidence_by_id_handler


class ClaimEvidenceHandler:
    create = staticmethod(create_claim_evidence_handler)
    get_all = staticmethod(get_all_claim_evidences_handler)
    get_by_id = staticmethod(get_claim_evidence_by_id_handler)
    download = staticmethod(download_claim_evidence_handler)
    delete = staticmethod(delete_claim_evidence_handler)


claimEvidenceHandler = ClaimEvidenceHandler()
