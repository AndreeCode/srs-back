from ....core.db.connection import get_connection
from ..domain.care_service_domain import CareService


async def update_care_service(care_service: CareService) -> CareService | None:
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            UPDATE care_services
            SET package_id = $1,
                code = $2,
                name = $3,
                group_name = $4,
                group_order = $5,
                sort_order = $6,
                min_age_days = $7,
                max_age_days = $8,
                min_interval_days = $9,
                active = $10
            WHERE id = $11
            RETURNING id, package_id, code, name,
                      group_name, group_order, sort_order,
                      min_age_days, max_age_days, min_interval_days, active,
                      created_at, updated_at
            """,
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
            care_service.id,
        )

        if row is None:
            return None

        return CareService.from_row(row)

    finally:
        await conn.close()
