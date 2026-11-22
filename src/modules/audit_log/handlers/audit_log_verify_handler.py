from ....core.db import audit_chain
from ....core.http.error import error
from ....core.http.succes import success
from ...security_alert.repositories.security_alert_repositories import securityAlertRepository


async def verify_and_alert() -> dict:
    result = await audit_chain.check_and_report()
    if not result["ok"]:
        await securityAlertRepository.save_alert(
            "audit_chain_broken",
            {
                "subject": f"seq-{result['broken_seq']}",
                "user_id": None,
                "device_hash": None,
                "detail": {"total": 1, "broken_seq": result["broken_seq"], "reason": result["reason"], "checked": result["checked"]},
            },
            0,
        )
    return result


async def verify_audit_chain_handler():
    try:
        result = await verify_and_alert()
        if result["ok"]:
            return success(200, f"Auditoria integra: {result['checked']} registros verificados", result)
        return success(200, f"La auditoria fue alterada en el registro {result['broken_seq']}: {result['reason']}", result)

    except Exception as err:
        return error(500, "Error al verificar la auditoria", err)
