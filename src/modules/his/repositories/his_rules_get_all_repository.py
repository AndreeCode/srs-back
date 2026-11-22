from ....core.db.connection import get_connection
from ..domain.his_domain import HisRule


async def get_all_his_rules() -> list[HisRule]:
    conn = await get_connection()

    try:
        rows = await conn.fetch(
            """
            SELECT his_code, dose_id, lab_value, service_id, priority
            FROM his_service_rules
            ORDER BY priority, id
            """
        )

        return [HisRule.from_row(row) for row in rows]

    finally:
        await conn.close()
