from .his_find_child_service import find_child
from .his_followup_service import followup


class HisService:
    find_child = staticmethod(find_child)
    followup = staticmethod(followup)


hisService = HisService()
