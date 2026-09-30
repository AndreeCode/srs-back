from ....core.db.connection import get_connection
from ..domain.care_service_domain import CareService


async def create_care_service(care_service: CareService) -> CareService:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            INSERT INTO care_services (
                id, package_id, code, name,
                group_name, group_order, sort_order,
                min_age_days, max_age_days, min_interval_days, active
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            RETURNING id, package_id, code, name,
                      group_name, group_order, sort_order,
                      min_age_days, max_age_days, min_interval_days, active,
                      created_at, updated_at
            """,
            care_service.id,
            care_service.package_id,
            care_service.code,
            care_service.name,
            care_service.group_name,
            care_service.group_order,
            care_service.sort_order,
            care_service.min_age_days,
            care_service.max_age_days,
            care_service.min_interval_days,
            care_service.active,
        )

        return CareService.from_row(row)

    finally:
        await conn.close()
