from ....core.db.connection import get_connection
from ..domain.care_package_domain import CarePackage


async def get_all_care_packages() -> list[CarePackage]:
    conn = await get_connection()

    try:
        rows = await conn.fetch(
            """
            SELECT id, code, name, description, min_age_days, max_age_days,
                   at_risk_newborn_only, sort_order, active, created_at, updated_at
            FROM care_packages
            WHERE active = true
            ORDER BY sort_order, min_age_days
            """
        )

        return [CarePackage.from_row(row) for row in rows]

    finally:
        await conn.close()
