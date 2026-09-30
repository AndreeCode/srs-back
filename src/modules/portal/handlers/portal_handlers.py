from .portal_claims_handler import portal_claim_create_handler, portal_claims_handler
from .portal_evidence_handler import portal_evidence_create_handler, portal_evidence_download_handler
from .portal_overview_handler import portal_overview_handler


class PortalHandler:
    overview = staticmethod(portal_overview_handler)
    claims = staticmethod(portal_claims_handler)
    create_claim = staticmethod(portal_claim_create_handler)
    upload_evidence = staticmethod(portal_evidence_create_handler)
    download_evidence = staticmethod(portal_evidence_download_handler)


portalHandler = PortalHandler()
