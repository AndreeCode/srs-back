from ....core.db.connection import get_connection
from ..domain.care_package_domain import CarePackage


async def update_care_package(care_package: CarePackage) -> CarePackage | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            UPDATE care_packages
            SET code = $1,
                name = $2,
                description = $3,
                min_age_days = $4,
                max_age_days = $5,
                at_risk_newborn_only = $6,
                sort_order = $7,
                active = $8
            WHERE id = $9
            RETURNING id, code, name, description, min_age_days, max_age_days,
                      at_risk_newborn_only, sort_order, active, created_at, updated_at
            """,
            care_package.code,
            care_package.name,
            care_package.description,
            care_package.min_age_days,
            care_package.max_age_days,
            care_package.at_risk_newborn_only,
            care_package.sort_order,
            care_package.active,
            care_package.id,
        )

        if row is None:
            return None

        return CarePackage.from_row(row)

    finally:
        await conn.close()
