import math
from datetime import date, timedelta

COMPLIANCE = {
    "PAD-0250317": 0.55,
    "PAD-0250334": 0.8,
    "PAD-0250351": 0.4,
    "PAD-0250368": 0.9,
    "PAD-0250385": 0.6,
    "PAD-0250402": 0.85,
    "PAD-0250419": 0.35,
    "PAD-0250436": 0.7,
    "PAD-0250453": 0.95,
    "PAD-0250470": 0.5,
    "PAD-0250487": 0.65,
    "PAD-0250504": 0.3,
    "PAD-0250521": 0.9,
    "PAD-0250538": 0.6,
    "PAD-0250555": 0.75,
    "PAD-0250572": 0.45,
    "PAD-0250589": 0.85,
    "PAD-0250606": 0.55,
    "PAD-0250623": 0.7,
    "PAD-0250640": 0.4,
    "PAD-0250657": 0.8,
    "PAD-0250674": 0.6,
    "PAD-0250691": 0.25,
    "PAD-0250708": 0.8,
}


def pseudo_random(a: int, b: int) -> float:
    x = math.sin(a * 12.9898 + b * 78.233) * 43758.5453
    return x - math.floor(x)


async def seed_child_controls(conn, children: dict, registered_by) -> None:
    services = await conn.fetch(
        """
        SELECT s.id, s.min_age_days, s.max_age_days, s.group_name,
               p.code AS package_code, p.min_age_days AS package_min, p.at_risk_newborn_only
        FROM care_services s JOIN care_packages p ON p.id = s.package_id
        WHERE s.active AND p.active
        ORDER BY p.sort_order, s.group_order, s.sort_order
        """
    )
    today = date.today()
    rows = []

    for child_index, (padron, compliance) in enumerate(COMPLIANCE.items(), start=1):
        child = children.get(padron)
        if child is None:
            continue

        age = (today - child["birth_date"]).days

        for service_index, service in enumerate(services, start=1):
            if service["at_risk_newborn_only"] and child["birth_condition"] == "none":
                continue
            if age < service["package_min"] or age < service["min_age_days"]:
                continue

            batch = f"L{2026000 + service_index * 7 + child_index}" if service["package_code"] == "INMUNIZACIONES" else None

            if pseudo_random(child_index, service_index) <= compliance:
                until = min(service["max_age_days"], age)
                day = service["min_age_days"] + math.floor(
                    pseudo_random(service_index, child_index) * max(0, until - service["min_age_days"])
                )
                notes = "Atención sin observaciones relevantes." if pseudo_random(child_index + 3, service_index) > 0.8 else None
                rows.append((child["id"], service["id"], "completed", None, child["birth_date"] + timedelta(days=day),
                             child["health_facility_id"], batch, notes))
            elif age <= service["max_age_days"] and pseudo_random(child_index + 7, service_index) > 0.5:
                scheduled = today + timedelta(days=1 + math.floor(pseudo_random(service_index, child_index + 7) * 20))
                rows.append((child["id"], service["id"], "pending", scheduled, None, child["health_facility_id"], None, None))

    await conn.executemany(
        """
        INSERT INTO child_controls (child_id, service_id, status, scheduled_date, completed_date,
                                    health_facility_id, batch_number, notes, registered_by)
        VALUES ($1, $2, $3::control_status, $4, $5, $6, $7, $8, $9)
        ON CONFLICT (child_id, service_id) DO NOTHING
        """,
        [(*row, registered_by) for row in rows],
    )
    completed = sum(1 for row in rows if row[2] == "completed")
    print(f"controles: {completed} cumplidos, {len(rows) - completed} citados")
