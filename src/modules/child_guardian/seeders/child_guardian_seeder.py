FAMILY = ["PAD-0250317", "PAD-0250334", "PAD-0250351"]

CHILD_GUARDIANS = [
    *[(padron, "40125896", "Madre") for padron in FAMILY],
    *[(padron, "41258963", "Padre") for padron in FAMILY],
    ("PAD-0250368", "40031676", "Madre"),
    ("PAD-0250385", "40039595", "Madre"),
    ("PAD-0250402", "40047514", "Madre"),
    ("PAD-0250419", "40055433", "Madre"),
    ("PAD-0250436", "40063352", "Madre"),
    ("PAD-0250453", "40071271", "Madre"),
    ("PAD-0250470", "40079190", "Madre"),
    ("PAD-0250487", "40087109", "Madre"),
    ("PAD-0250504", "40095028", "Madre"),
    ("PAD-0250521", "40102947", "Madre"),
    ("PAD-0250538", "40110866", "Madre"),
    ("PAD-0250555", "40118785", "Madre"),
    ("PAD-0250572", "40126704", "Madre"),
    ("PAD-0250589", "40134623", "Madre"),
    ("PAD-0250606", "40142542", "Madre"),
    ("PAD-0250623", "40150461", "Madre"),
    ("PAD-0250640", "40158380", "Madre"),
    ("PAD-0250657", "40166299", "Madre"),
    ("PAD-0250674", "40174218", "Madre"),
    ("PAD-0250691", "40182137", "Madre"),
    ("PAD-0250708", "40190056", "Madre"),
]


async def seed_child_guardians(conn, children: dict, guardian_ids: dict) -> None:
    await conn.executemany(
        """
        INSERT INTO child_guardian (child_id, guardian_id, relationship) VALUES ($1, $2, $3)
        ON CONFLICT DO NOTHING
        """,
        [(children[padron]["id"], guardian_ids[dni], relationship) for padron, dni, relationship in CHILD_GUARDIANS],
    )
    print(f"vínculos padre-hijo: {len(CHILD_GUARDIANS)}")
