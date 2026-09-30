import argparse
import asyncio
import sys

from scripts import migrate, reset


async def main(yes: bool, seed: bool) -> int:
    if await reset.main(drop=True, yes=yes, hint=False) != 0:
        return 1

    print()
    if await migrate.main() != 0:
        return 1

    if seed:
        print()
        from scripts import seed as seed_script

        if await seed_script.main() != 0:
            return 1

    print("\nDatabase recreated from scratch.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Drops the whole schema and runs the migration again.")
    parser.add_argument("--yes", action="store_true", help="do not ask for confirmation")
    parser.add_argument("--seed", action="store_true", help="then load the seed data (scripts.seed)")
    args = parser.parse_args()
    sys.exit(asyncio.run(main(args.yes, args.seed)))
