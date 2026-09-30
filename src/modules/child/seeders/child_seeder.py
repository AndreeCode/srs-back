from datetime import date, timedelta

CHILDREN = [
    ("PAD-0250317", "Valentina", "Cárdenas Huamán", "F", 250, "90104729", "none", "María Huamán Quispe", "40125896", "951037321", "Belén"),
    ("PAD-0250334", "Mateo", "Cárdenas Huamán", "M", 1150, "90209458", "none", "María Huamán Quispe", "40125896", "951074642", "Belén"),
    ("PAD-0250351", "Luciana", "Cárdenas Huamán", "F", 20, "90314187", "premature", "María Huamán Quispe", "40125896", "951111963", "Belén"),
    ("PAD-0250368", "Diego", "Rojas Palomino", "M", 12, None, "none", "Carmen Palomino Soto", "40031676", "951149284", "Barrios Altos"),
    ("PAD-0250385", "Camila", "Quispe Llamocca", "F", 45, "90523645", "low_weight", "Rosa Llamocca Pariona", "40039595", "951186605", "Huascahura"),
    ("PAD-0250402", "Thiago", "Gamboa Ccori", "M", 100, "90628374", "none", "Julia Ccori Tineo", "40047514", "951223926", "Santa Ana"),
    ("PAD-0250419", "Sofía", "Pariona Yupanqui", "F", 170, "90733103", "none", "Elena Yupanqui Mendoza", "40055433", "951261247", "Carmen Alto"),
    ("PAD-0250436", "Santiago", "Mendoza Ayala", "M", 320, "90837832", "none", "Lucía Ayala Prado", "40063352", "951298568", "Vista Alegre"),
    ("PAD-0250453", "Isabella", "Tineo Barboza", "F", 400, "90942561", "none", "Carla Barboza Janampa", "40071271", "951335889", "Yanama"),
    ("PAD-0250470", "Gael", "Huamaní Cisneros", "M", 500, "91047290", "none", "Nancy Cisneros Ore", "40079190", "951373210", "Chiara"),
    ("PAD-0250487", "Ariana", "Janampa Vila", "F", 620, "91152019", "premature", "Pilar Vila Gutiérrez", "40087109", "951410531", "Allpachaca"),
    ("PAD-0250504", "Adrián", "Ore Sulca", "M", 700, "91256748", "none", "Yolanda Sulca Ramos", "40095028", "951447852", "Chontaca"),
    ("PAD-0250521", "Emma", "Gutiérrez Pillaca", "F", 800, "91361477", "none", "Silvia Pillaca Díaz", "40102947", "951485173", "Acocro"),
    ("PAD-0250538", "Lucas", "Ramos Chávez", "M", 900, "91466206", "none", "Doris Chávez León", "40110866", "951522494", "Licenciados"),
    ("PAD-0250555", "Mía", "Díaz Quicaño", "F", 1000, "91570935", "none", "Gloria Quicaño Bautista", "40118785", "951559815", "Centro de Salud Nazareno"),
    ("PAD-0250572", "Benjamín", "León Ñaupa", "M", 1300, "91675664", "none", "Irma Ñaupa Huayta", "40126704", "951597136", "Mollepata"),
    ("PAD-0250589", "Renata", "Bautista Ccente", "F", 1500, "91780393", "none", "Flor Ccente Arango", "40134623", "951634457", "Muyurina"),
    ("PAD-0250606", "Joaquín", "Huayta Palomino", "M", 1700, "91885122", "none", "Martha Palomino Rojas", "40142542", "951671778", "Pacaycasa"),
    ("PAD-0250623", "Antonella", "Arango Cuba", "F", 1900, "91989851", "none", "Rocío Cuba Sánchez", "40150461", "951709099", "Simpapata"),
    ("PAD-0250640", "Dylan", "Sánchez Taipe", "M", 2300, "92094580", "none", "Lourdes Taipe Mitma", "40158380", "951746420", "Barrios Altos"),
    ("PAD-0250657", "Valeria", "Mitma Condori", "F", 2800, "92199309", "none", "Norma Condori Huillca", "40166299", "951783741", "Huascahura"),
    ("PAD-0250674", "Samuel", "Condori Galindo", "M", 3200, "92304038", "none", "Betty Galindo Poma", "40174218", "951821062", "Santa Ana"),
    ("PAD-0250691", "Zoe", "Poma Rivera", "F", 360, "92408767", "none", "Ana Rivera Loayza", "40182137", "951858383", "Belén"),
    ("PAD-0250708", "Leonardo", "Loayza Paucar", "M", 60, "92513496", "none", "Carmen Paucar Villa", "40190056", "951895704", "Barrios Altos"),
]


async def seed_children(conn, facility_ids: dict, registered_by) -> dict[str, dict]:
    today = date.today()

    await conn.executemany(
        """
        INSERT INTO children (padron_code, first_names, last_names, gender, birth_date, dni, birth_condition,
                              mother_name, mother_dni, contact_phone, insurance, health_facility_id, registered_by)
        VALUES ($1, $2, $3, $4, $5, $6, $7::birth_condition, $8, $9, $10, 'SIS', $11, $12)
        ON CONFLICT (padron_code) DO NOTHING
        """,
        [
            (padron, first, last, gender, today - timedelta(days=age), dni, condition, mother, mother_dni, phone,
             facility_ids[facility], registered_by)
            for padron, first, last, gender, age, dni, condition, mother, mother_dni, phone, facility in CHILDREN
        ],
    )

    codes = [child[0] for child in CHILDREN]
    rows = await conn.fetch(
        """
        SELECT id, padron_code, dni, birth_date, birth_condition::text AS birth_condition, health_facility_id
        FROM children WHERE padron_code = ANY($1::text[])
        """,
        codes,
    )
    print(f"niños: {len(rows)}")
    return {row["padron_code"]: dict(row) for row in rows}
