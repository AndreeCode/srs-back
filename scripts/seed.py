import argparse
import asyncio
import sys

from src.core.config.config import config
from src.core.db.connection import get_connection
from src.modules.care_package.seeders.care_package_seeder import seed_care_packages
from src.modules.care_service.seeders.care_service_seeder import seed_care_services
from src.modules.child.seeders.child_seeder import seed_children
from src.modules.child_control.seeders.child_control_seeder import seed_child_controls
from src.modules.child_guardian.seeders.child_guardian_seeder import seed_child_guardians
from src.modules.claim.seeders.claim_seeder import seed_claims
from src.modules.claim_evidence.seeders.claim_evidence_seeder import seed_claim_evidences
from src.modules.guardian.seeders.guardian_seeder import seed_guardian_accounts, seed_guardians
from src.modules.health_facility.seeders.health_facility_seeder import seed_health_facilities
from src.modules.his.seeders.his_seeder import seed_his_rules
from src.modules.permission.seeders.permission_seeder import seed_permissions
from src.modules.region.seeders.region_seeder import seed_regions
from src.modules.role.seeders.role_seeder import seed_roles
from src.modules.user.seeders.user_seeder import seed_users
from src.modules.user_region.seeders.user_region_seeder import seed_user_regions


async def main(demo: bool = True) -> int:
    conn = await get_connection()

    try:
        async with conn.transaction():
            role_ids = await seed_roles(conn)
            await seed_permissions(conn, role_ids)
            user_ids = await seed_users(conn, role_ids)

            region_ids = await seed_regions(conn)
            facility_ids = await seed_health_facilities(conn, region_ids)
            await seed_user_regions(conn, user_ids, region_ids)

            package_ids = await seed_care_packages(conn)
            service_ids = await seed_care_services(conn, package_ids)
            await seed_his_rules(conn)

            if demo:
                guardian_ids = await seed_guardians(conn, user_ids)
                await seed_guardian_accounts(conn, role_ids["guardian"])
                children = await seed_children(conn, facility_ids, user_ids["admin"])
                await seed_child_guardians(conn, children, guardian_ids)
                await seed_child_controls(conn, children, user_ids["admin"])
                claim_ids = await seed_claims(conn, children, user_ids, facility_ids, service_ids)
                await seed_claim_evidences(conn, claim_ids)

    except Exception as e:
        first = str(e).splitlines()[0] if str(e) else type(e).__name__
        print(f"\nSeed failed, nothing was saved: {first}")
        return 1

    finally:
        await conn.close()

    print("\nSeed completed.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Loads roles, permissions, users, territory, CRED catalog and demo data.")
    parser.add_argument("--no-demo", action="store_true", help="skip demo guardians, children, controls and claims")
    args = parser.parse_args()
    if config.is_production and not args.no_demo:
        print("APP_ENV=production: demo data is disabled, use --no-demo")
        sys.exit(1)
    sys.exit(asyncio.run(main(demo=not args.no_demo)))
