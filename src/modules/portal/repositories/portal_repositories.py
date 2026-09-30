from .portal_children_repository import get_children_of_guardian
from .portal_guardian_repository import get_guardian_by_user


class PortalRepository:
    get_guardian_by_user = staticmethod(get_guardian_by_user)
    get_children_of_guardian = staticmethod(get_children_of_guardian)


portalRepository = PortalRepository()
