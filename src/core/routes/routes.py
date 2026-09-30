from fastapi import APIRouter

from ...modules.audit_log.audit_log_route import router as audit_log_router
from ...modules.auth.auth_route import router as auth_router
from ...modules.care_package.care_package_route import router as care_package_router
from ...modules.care_service.care_service_route import router as care_service_router
from ...modules.child.child_route import router as child_router
from ...modules.child_guardian.child_guardian_route import router as child_guardian_router
from ...modules.child_control.child_control_route import router as child_control_router
from ...modules.claim.claim_route import router as claim_router
from ...modules.claim_evidence.claim_evidence_route import router as claim_evidence_router
from ...modules.device.device_route import router as device_router
from ...modules.guardian.guardian_route import router as guardian_router
from ...modules.health_facility.health_facility_route import router as health_facility_router
from ...modules.permission.permission_route import router as permission_router
from ...modules.portal.portal_route import router as portal_router
from ...modules.region.region_route import router as region_router
from ...modules.security_alert.security_alert_route import router as security_alert_router
from ...modules.role.role_route import router as role_router
from ...modules.session.session_route import router as session_router
from ...modules.user.user_route import router as user_router
from ...modules.user_region.user_region_route import router as user_region_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(role_router)
router.include_router(user_router)
router.include_router(permission_router)
router.include_router(guardian_router)
router.include_router(region_router)
router.include_router(health_facility_router)
router.include_router(user_region_router)
router.include_router(child_router)
router.include_router(child_guardian_router)
router.include_router(care_package_router)
router.include_router(care_service_router)
router.include_router(child_control_router)
router.include_router(claim_router)
router.include_router(claim_evidence_router)
router.include_router(device_router)
router.include_router(session_router)
router.include_router(audit_log_router)
router.include_router(portal_router)
router.include_router(security_alert_router)
