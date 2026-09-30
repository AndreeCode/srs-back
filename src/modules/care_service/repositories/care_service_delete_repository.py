from uuid import UUID

from ....core.db.connection import get_connection


async def delete_care_service(care_service_id: UUID) -> str:
    conn = await get_connection()

    try:
        in_use = await conn.fetchval(
            """
            SELECT EXISTS (SELECT 1 FROM child_controls WHERE service_id = $1)
                OR EXISTS (SELECT 1 FROM claims WHERE service_id = $1)
            """,
            care_service_id,
        )

        if not in_use:
            result = await conn.execute("DELETE FROM care_services WHERE id = $1", care_service_id)
            return "not_found" if result.endswith(" 0") else "deleted"

        result = await conn.execute(
            "UPDATE care_services SET active = false WHERE id = $1",
            care_service_id,
        )
        return "not_found" if result.endswith(" 0") else "deactivated"

    finally:
        await conn.close()
