from uuid import UUID

from ....core.db.connection import get_connection


async def delete_care_package(care_package_id: UUID) -> str:
    conn = await get_connection()

    try:
        in_use = await conn.fetchval(
            "SELECT EXISTS (SELECT 1 FROM care_services WHERE package_id = $1)",
            care_package_id,
        )

        if not in_use:
            result = await conn.execute("DELETE FROM care_packages WHERE id = $1", care_package_id)
            return "not_found" if result.endswith(" 0") else "deleted"

        result = await conn.execute(
            "UPDATE care_packages SET active = false WHERE id = $1",
            care_package_id,
        )
        return "not_found" if result.endswith(" 0") else "deactivated"

    finally:
        await conn.close()
