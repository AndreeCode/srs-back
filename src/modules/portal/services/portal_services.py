from .portal_claims_service import create_claim, get_evidence, list_claims, upload_evidence
from .portal_link_child_service import link_child
from .portal_overview_service import overview


class PortalService:
    overview = staticmethod(overview)
    list_claims = staticmethod(list_claims)
    create_claim = staticmethod(create_claim)
    upload_evidence = staticmethod(upload_evidence)
    get_evidence = staticmethod(get_evidence)
    link_child = staticmethod(link_child)


portalService = PortalService()
