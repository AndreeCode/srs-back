from uuid import UUID

from ....core.db.connection import get_connection
from ..domain.care_package_domain import CarePackage


async def get_care_package_by_id(care_package_id: UUID) -> CarePackage | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            SELECT id, code, name, description, min_age_days, max_age_days,
                   at_risk_newborn_only, sort_order, active, created_at, updated_at
            FROM care_packages
            WHERE id = $1
            """,
            care_package_id,
        )

        if row is None:
            return None

        return CarePackage.from_row(row)

    finally:
        await conn.close()
