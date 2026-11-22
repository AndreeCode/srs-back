from uuid import UUID

from ...care_package.services.care_packages_service import carePackageService
from ...care_service.services.care_services_service import careServiceService
from ..domain.his_domain import EARLY_TOLERANCE_DAYS, HisAttention, HisChild, HisRule, birth_condition
from ..repositories.his_repositories import hisRepository


def map_controls(
    child: HisChild,
    attentions: list[HisAttention],
    rules: list[HisRule],
    services: dict,
    packages: dict,
    condition: str,
) -> list[dict]:
    by_code: dict[str, list[HisRule]] = {}
    for rule in rules:
        by_code.setdefault(rule.his_code.upper(), []).append(rule)

    assigned: dict[UUID, dict] = {}
    for attention in attentions:
        age = (attention.attention_date - child.birth_date).days
        used_packages: set[UUID] = set()

        for rule in by_code.get(attention.code.upper(), []):
            if rule.service_id in assigned:
                continue
            if rule.dose_id is not None and rule.dose_id != attention.dose_id:
                continue
            if rule.lab_value is not None and (attention.lab_value or "").upper() != rule.lab_value.upper():
                continue

            service = services.get(rule.service_id)
            package = packages.get(service.package_id) if service else None
            if service is None or package is None or not service.active or not package.active:
                continue
            if package.at_risk_newborn_only and condition == "none":
                continue
            if not service.min_age_days - EARLY_TOLERANCE_DAYS <= age <= service.max_age_days:
                continue
            if package.id in used_packages:
                continue

            used_packages.add(package.id)
            assigned[rule.service_id] = {
                "id": f"{child.portal_id}-{rule.service_id}",
                "source": "his",
                "child_id": child.portal_id,
                "service_id": str(rule.service_id),
                "status": "completed",
                "scheduled_date": None,
                "completed_date": attention.attention_date.isoformat(),
                "health_facility_id": None,
                "facility_name": attention.facility_name,
                "batch_number": attention.batch,
                "book_page": attention.page,
                "book_record": attention.record,
                "notes": attention.notes(),
                "registered_by": None,
                "created_at": None,
                "updated_at": None,
            }

    return list(assigned.values())


def child_dict(child: HisChild, condition: str, attentions: int, child_name: str | None, relationship: str | None) -> dict:
    return {
        "id": child.portal_id,
        "source": "his",
        "padron_code": child.document_number,
        "medical_record_code": None,
        "dni": child.document_number,
        "document_type": child.document_type,
        "first_names": child_name or f"{child.document_type} {child.document_number}",
        "last_names": "",
        "birth_date": child.birth_date.isoformat(),
        "gender": child.gender,
        "birth_condition": condition,
        "mother_name": None,
        "mother_dni": None,
        "address": None,
        "contact_phone": None,
        "insurance": None,
        "health_facility_id": None,
        "facility_name": child.facility_name,
        "micro_red": child.micro_red,
        "active": True,
        "relationship": relationship,
        "attentions": attentions,
    }


async def followup(links: list[dict], with_attentions: bool = False) -> dict:
    if not links:
        return {"children": [], "controls": [], "attentions": {}}

    found = await hisRepository.find_children([link["document_number"] for link in links])
    patient_to_document = {pid: doc for doc, child in found.items() for pid in child.patient_ids}
    all_attentions = await hisRepository.get_attentions(list(patient_to_document))

    by_document: dict[str, list[HisAttention]] = {}
    for attention in all_attentions:
        by_document.setdefault(patient_to_document[attention.patient_id], []).append(attention)

    rules = await hisRepository.get_rules()
    services = {service.id: service for service in await careServiceService.get_all(None)}
    packages = {package.id: package for package in await carePackageService.get_all()}

    children, controls, attentions = [], [], {}
    for link in links:
        child = found.get(link["document_number"])
        if child is None:
            continue
        own = by_document.get(child.document_number, [])
        condition = birth_condition(own)
        children.append(child_dict(child, condition, len(own), link.get("child_name"), link.get("relationship")))
        controls += map_controls(child, own, rules, services, packages, condition)
        if with_attentions:
            attentions[child.portal_id] = [attention.to_dict() for attention in own]

    return {"children": children, "controls": controls, "attentions": attentions}
