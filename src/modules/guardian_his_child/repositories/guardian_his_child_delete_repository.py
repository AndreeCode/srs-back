from uuid import UUID

from ....core.db.connection import get_connection


async def delete_guardian_his_child(guardian_id: UUID, document_number: str) -> str:
    conn = await get_connection()

    try:
        result = await conn.execute(
            "DELETE FROM guardian_his_children WHERE guardian_id = $1 AND document_number = $2",
            guardian_id,
            document_number,
        )

        return "deleted" if result.endswith(" 1") else "not_found"

    finally:
        await conn.close()
