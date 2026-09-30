from ....core.db.connection import get_connection
from ..domain.care_package_domain import CarePackage


async def create_care_package(care_package: CarePackage) -> CarePackage:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            INSERT INTO care_packages (
                id, code, name, description, min_age_days, max_age_days,
                at_risk_newborn_only, sort_order, active
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            RETURNING id, code, name, description, min_age_days, max_age_days,
                      at_risk_newborn_only, sort_order, active, created_at, updated_at
            """,
            care_package.id,
            care_package.code,
            care_package.name,
            care_package.description,
            care_package.min_age_days,
            care_package.max_age_days,
            care_package.at_risk_newborn_only,
            care_package.sort_order,
            care_package.active,
        )

        return CarePackage.from_row(row)

    finally:
        await conn.close()
