from uuid import UUID

from ....core.db.connection import get_connection


async def delete_health_facility(health_facility_id: UUID) -> str:
    conn = await get_connection()

    try:
        in_use = await conn.fetchval(
            "SELECT EXISTS (SELECT 1 FROM children WHERE health_facility_id = $1)",
            health_facility_id,
        )

        if not in_use:
            result = await conn.execute("DELETE FROM health_facilities WHERE id = $1", health_facility_id)
            return "not_found" if result.endswith(" 0") else "deleted"

        result = await conn.execute(
            "UPDATE health_facilities SET active = false WHERE id = $1",
            health_facility_id,
        )
        return "not_found" if result.endswith(" 0") else "deactivated"

    finally:
        await conn.close()
