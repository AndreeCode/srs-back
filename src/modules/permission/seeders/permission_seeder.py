from ..domain.permission_catalog import PERMISSIONS

FULL_ACCESS_ROLES = ["admin"]

ROLE_PERMISSIONS = {
    "health_staff": [
        "user.get:me",
        "guardian.get",
        "guardian.post",
        "guardian.put",
        "guardian.delete",
        "child.get",
        "child.post",
        "child.put",
        "child.delete",
        "child_guardian.get",
        "child_guardian.post",
        "child_guardian.put",
        "child_guardian.delete",
        "child_control.get",
        "child_control.post",
        "child_control.put",
        "child_control.delete",
        "claim.get",
        "claim.put",
        "claim_evidence.get",
        "care_package.get",
        "care_service.get",
        "health_facility.get",
        "region.get",
    ],
    "guardian": ["user.get:me", "portal.get", "portal.post"],
}


async def grant(conn, role_id, codes: list[str]) -> None:
    await conn.execute(
        """
        INSERT INTO role_permission (role_id, permission_id)
        SELECT $1, id FROM permissions WHERE code = ANY($2::text[])
        ON CONFLICT DO NOTHING
        """,
        role_id,
        codes,
    )


async def seed_permissions(conn, role_ids: dict) -> None:
    await conn.executemany(
        """
        INSERT INTO permissions (code, description) VALUES ($1, $2)
        ON CONFLICT (code) DO UPDATE SET description = EXCLUDED.description
        WHERE permissions.description IS DISTINCT FROM EXCLUDED.description
        """,
        list(PERMISSIONS.items()),
    )

    for name in FULL_ACCESS_ROLES:
        await grant(conn, role_ids[name], list(PERMISSIONS))
        print(f"permisos: {len(PERMISSIONS)} -> rol {name}")

    for name, codes in ROLE_PERMISSIONS.items():
        await grant(conn, role_ids[name], codes)
        print(f"permisos: {', '.join(codes)} -> rol {name}")
